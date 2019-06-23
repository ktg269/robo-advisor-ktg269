

from app/robo_advisor.py import 


while True:
        
    if receipt_print =="y":   # sending email receipt
        
        user_input = input("PLEASE ENTER YOUR EMAIL ADDRESS: ") # asking user email address for input.    

        import os
        from dotenv import load_dotenv
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail

        load_dotenv()

        SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", "OOPS, please set env var called 'SENDGRID_API_KEY'")  #private information included in .env
        SENDGRID_TEMPLATE_ID = os.environ.get("SENDGRID_TEMPLATE_ID", "OOPS, please set env var called 'SENDGRID_TEMPLATE_ID'") #private information included in .env
        MY_ADDRESS = os.environ.get("MY_EMAIL_ADDRESS", "OOPS, please set env var called 'MY_EMAIL_ADDRESS'") #private information included in .env

        template_data = {   # showing the checkout timestamp and the total price on the email receipt (minimum level of information per instruction)
            "total_price_usd": str(to_usd(total_price)),
            "human_friendly_timestamp": str(t.strftime("%Y-%m-%d %I:%M %p")),

        }
        client = SendGridAPIClient(SENDGRID_API_KEY) #> <class 'sendgrid.sendgrid.SendGridAPIClient>
        print("CLIENT:", type(client))

        message = Mail(from_email=MY_ADDRESS, to_emails=user_input) # For to_emails, MY_ADDRESS is replaced with user_input from line 133.
        print("MESSAGE:", type(message))
        message.template_id = SENDGRID_TEMPLATE_I
        message.dynamic_template_data = template_dat
        try:
            response = client.send(message)
            print("RESPONSE:", type(response)) #> <class 'python_http_client.client.Response'>
            print(response.status_code) #> 202 indicates SUCCESS
            print(response.body)
            print(response.headers
        except Exception as e:
            print("OOPS", e.message)
        print("YOUR RECEIPT HAS BEEN SENT. THANK YOU AND WE HOPE TO SEE YOU AGAIN !") # A friendly message thanking the customer and/or encouraging the customer to shop again
        break

    else:
        print("PLEASE TAKE YOUR PAPER RECEIPT. THANK YOU AND WE HOPE TO SEE YOU AGAIN !") # No email receipt if customer does not select y.
        break

