import json
import boto3


def lambda_handler(event, context):
    # TODO implement
    print("This is Event: ",event)
    
    #print("event['Records'][0]['body'] :",event['Records'][0]['body'])
    
    def taxAndDiscount(val):
        if val > 200 and val < 500: 
            return val//100, 50  # here tax is val//100, and 50 is discount
        if val > 500 and val < 700: 
            return val//80, 100
        if val > 700 and val < 1000:
            return val//60, 150
        if val > 1000 :
            return val//50, 250
        return 0,5
        
    try :
    
        order_details = json.loads(event['Records'][0]['body'])
        
        print("order_details: ", order_details)
        
        tax, discount = taxAndDiscount(int(order_details['total amount']))
        
        print("Tax: {}, Discount: {}". format(tax, discount))
        
        order_details['Tax'] = tax
        order_details['Discount'] = discount
        order_details['FinalAmount'] = int(order_details['total amount']) + order_details['Tax'] - order_details['Discount']
        
        s3client = boto3.client("s3")
        s3client.put_object( Bucket='zensarinvoices', Key=order_details['order ID']+'_invoice.json',Body=json.dumps(order_details) )
        
    except Exception as e:
        print("There is an error and error is: ", e) 
    

