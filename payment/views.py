from django.shortcuts import render, redirect, get_object_or_404
import logging
from django.contrib.auth.decorators import login_required
from .models import Payment
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from order.models import Order
import uuid
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.db import transaction

# Set up logging
logger = logging.getLogger(__name__)

@login_required
def create_payment(request):
    logger.info(f"Payment creation request from user: {request.user}")
    if request.method == 'POST':
        try:
            amount = request.POST.get('amount')
            payment_mode = request.POST.get('payment_mode')
            upi_id = request.POST.get('upi_id') if payment_mode == 'UPI' else None
            
            logger.info(f"Creating payment with amount: {amount}, mode: {payment_mode}, UPI ID: {upi_id}")
            payment = Payment.objects.create(
                user=request.user,
                amount=amount,
                payment_mode=payment_mode,
                upi_id=upi_id,
                payment_status='COMPLETED' if payment_mode == 'CASH' else 'PENDING'
            )

            if payment_mode == 'CASH':
                payment.mark_as_paid()
                messages.success(request, 'Payment completed successfully!')
                return redirect('payment:payment_success')
            
            return redirect('payment:verify_payment', payment_id=payment.id)

        except Exception as e:
            logger.error(f"Error creating payment: {str(e)}")
            messages.error(request, f'Error processing payment: {str(e)}')
            return redirect('chai:all_chai')

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def verify_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    
    if request.method == 'POST':
        try:
            # Add verification logic here (e.g., check callback from payment gateway)
            payment.mark_as_paid()
            messages.success(request, 'Payment verified successfully!')
            return redirect('payment:payment_success')
        except Exception as e:
            logger.error(f"Error verifying payment {payment_id}: {str(e)}")
            payment.mark_as_failed()
            messages.error(request, 'Payment verification failed. Please try again.')
            return redirect('chai:all_chai')
    
    return render(request, 'payment/verify_payment.html', {'payment': payment})

def payment_process(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    order = payment.order
    
    if request.method == 'POST':
        try:
            if payment.payment_mode == 'UPI':
                # Generate a dummy UPI ID for demonstration
                payment.upi_id = f"demo.upi.{uuid.uuid4().hex[:8]}"
                payment.save()
                return redirect('payment:verify_upi', payment_id=payment.id)
            elif payment.payment_mode == 'CASH':
                payment.payment_status = 'PENDING_DELIVERY'
                order.payment_status = 'unpaid'  # Will be paid on delivery
                payment.save()
                order.save()
                messages.success(request, 'Order placed successfully! Pay on delivery.')
                return redirect('payment:payment_success')
        except Exception as e:
            logger.error(f"Error processing payment {payment_id}: {str(e)}")
            payment.mark_as_failed()
            messages.error(request, 'Payment processing failed. Please try again.')
            return redirect('chai:all_chai')
    
    return render(request, 'payment/process_payment.html', {
        'payment': payment,
        'order': order
    })

def verify_upi(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    order = payment.order
    
    if request.method == 'POST':
        try:
            upi_transaction_id = request.POST.get('upi_transaction_id')
            if not upi_transaction_id:
                raise ValueError('UPI Transaction ID is required')
            
            payment.transaction_id = upi_transaction_id
            payment.mark_as_paid()
            messages.success(request, 'Payment completed successfully!')
            return redirect('payment:payment_success')
        except Exception as e:
            logger.error(f"Error verifying UPI payment {payment_id}: {str(e)}")
            payment.mark_as_failed()
            messages.error(request, 'UPI verification failed. Please try again.')
            return redirect('chai:all_chai')
    
    return render(request, 'payment/verify_upi.html', {
        'payment': payment,
        'order': order,
        'upi_id': payment.upi_id
    })

@login_required
def payment_options(request, order_id):
    """Single entry point for payment flow"""
    order = get_object_or_404(Order.objects.select_related('payment'), id=order_id)
    payment = order.payment

    if order.payment_status == 'paid':
        return redirect('order:order_detail', order_id=order.id)
    
    if request.method == 'POST':
        payment_mode = request.POST.get('payment_mode')
        if not payment_mode:
            messages.error(request, 'Please select a payment method.')
            return redirect('payment:payment_options', order_id=order.id)
        
        try:
            with transaction.atomic():
                payment.payment_mode = payment_mode
                payment.transaction_id = f"CHAI-{uuid.uuid4().hex[:8].upper()}"
                
                if payment_mode == 'CASH':
                    # Immediately process cash payments
                    payment.payment_status = 'PENDING_DELIVERY'
                    payment.save()
                    order.payment_status = 'unpaid'
                    order.save()
                    messages.success(request, 'Order placed successfully! Please pay cash on delivery.')
                    return redirect('order:order_detail', order_id=order.id)
                else:
                    # For UPI, CARD, or WALLET payments - redirect to gateway
                    payment.save()
                    return redirect('payment:payment_gateway', payment_id=payment.id)
                    
        except Exception as e:
            logger.error(f"Error processing payment for order {order_id}: {str(e)}")
            messages.error(request, 'Error processing payment. Please try again.')
            return redirect('payment:payment_options', order_id=order.id)
    
    context = {
        'order': order,
        'payment': payment,
        'payment_modes': Payment.PAYMENT_MODES,
    }
    return render(request, 'payment/payment_options.html', context)

@login_required
@require_http_methods(['POST'])
def process_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    payment_mode = request.POST.get('payment_mode')
    
    if not payment_mode:
        messages.error(request, 'Please select a payment method.')
        return redirect('payment:payment_options', order_id=order.id)
    
    # Create payment record
    payment = Payment.objects.create(
        user=request.user,
        amount=order.total_price,
        payment_mode=payment_mode,
        transaction_id=f"CHAI-{uuid.uuid4().hex[:8].upper()}",
    )
    
    # Link payment to order
    order.payment = payment
    order.save()
    
    # Simulate payment processing based on payment mode
    if payment_mode == 'CASH':
        # For cash payments, mark as pending delivery
        payment.payment_status = 'PENDING_DELIVERY'
        payment.save()
        messages.success(request, 'Order placed successfully! Please pay cash on delivery.')
        return redirect('order:order_detail', order_id=order.id)
    
    elif payment_mode in ['UPI', 'CARD', 'WALLET']:
        # Redirect to payment gateway (simulated)
        return redirect('payment:payment_gateway', payment_id=payment.id)
    
    messages.error(request, 'Invalid payment method selected.')
    return redirect('payment:payment_options', order_id=order.id)

@login_required
def payment_gateway(request, payment_id):
    """Handle all non-cash payments"""
    payment = get_object_or_404(Payment.objects.select_related('order'), id=payment_id)
    order = payment.order
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                if payment.payment_mode == 'UPI':
                    # Handle UPI-specific logic
                    upi_transaction_id = request.POST.get('upi_transaction_id')
                    if not upi_transaction_id:
                        raise ValueError('UPI Transaction ID is required')
                    payment.transaction_id = upi_transaction_id
                
                # Complete the payment
                payment.payment_status = 'COMPLETED'
                payment.is_paid = True
                payment.save()
                
                order.payment_status = 'paid'
                order.save()
                
                messages.success(request, 'Payment successful! Your order has been confirmed.')
                # Redirect to payment success page instead of order detail
                return redirect('payment:payment_success')
                
        except Exception as e:
            logger.error(f"Error processing payment at gateway {payment_id}: {str(e)}")
            messages.error(request, 'Payment processing failed. Please try again.')
            return redirect('payment:payment_options', order_id=order.id)
    
    context = {
        'payment': payment,
        'order': order,
        'is_upi': payment.payment_mode == 'UPI'
    }
    return render(request, 'payment/payment_gateway.html', context)

def payment_success(request):
    """Simple success page after payment completion"""
    return render(request, 'payment/success.html')
