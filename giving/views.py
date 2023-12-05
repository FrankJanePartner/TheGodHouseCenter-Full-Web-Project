from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
# from pypaystack import Transaction, Customer, plan
from django.conf import settings

# Create your views here.
def giving(request):
    return render(request, 'giving.html')

# #a view for implementing paystack
# # payment gateway
# from django.http import HttpResponseRedirect
# from django.conf import settings
# import paystack
# def paystack_payment(request):
#     # Create an instance of the Paystack API
#     api = paystack.PaystackAPI(settings.PAYSTACK_SECRET_KEY)
    
#     # Set up a transaction object with all required parameters
#     transaction = paystack.Transaction({
#         "email": request.POST.get('email'),
#         "amount": request.POST.get('amount'),
#         "reference": request.POST.get('reference'),
#         "callback_url": request.build_absolute_uri(
#             reverse('paystack_callback')),
#             })
    
#     # Make a request to the Paystack API to initiate the transaction
#     response = api.transaction.initialize(transaction)
#     # If the transaction is successful, redirect the user to the Paystack payment page
#     if response.status == True:
#         return HttpResponseRedirect(response.data.get('authorization_url'))
    
#     else:
#         return render(request, 'paystack.html', {'error': response.message})

# # This view is called when the Paystack payment page redirects the user back to your site
# # It's responsible for verifying the transaction and updating the user's account balance
# def paystack_callback(request):
#     # Create an instance of the Paystack API    api = paystack.PaystackAPI(settings.PAYSTACK_SECRET_KEY)
#     api = paystack.PaystackAPI(settings.PAYSTACK_SECRET_KEY)
#     # Get the transaction reference from the Paystack callback
#     reference = request.GET.get('reference')
#     # Verify the transaction with the Paystack API
#     response = api.transaction.verify(reference)
#     # If the transaction is successful, update the user's account balance
#     if response.status == True:
#         # Get the user's account balance
#         current_balance = get_user_account_balance()
#         # Add the transaction amount to the user's account balance
#         new_balance = current_balance + int(response.data.get('amount'))
#         # Update the user's account balance
#         update_user_account_balance(new_balance)
#         # Redirect the user to a success page
#         return render(request, 'paystack_success.html')
    