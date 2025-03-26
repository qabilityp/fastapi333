from pywa import WhatsApp

#store token and id numbers in .env

wa = WhatsApp(
    phone_id='YOUR_PHONE_ID',
    token='YOUR_TOKEN',
)

wa.send_message(
    to='recipient',
    text='Hi! This message was sent from pywa!'
)

wa.send_image(
    to='recipient',
    image='https://www.rd.com/wp-content/uploads/2021/04/GettyImages-1053735888-scaled.jpg'
)
