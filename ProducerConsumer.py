import requests
from bs4 import BeautifulSoup
import json
import time
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError

# Scrape data from the website
url = "https://scrapeme.live/shop/"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

items = []
for product in soup.select(".product"):
    link=product.select_one("a")["href"]
    response = requests.get(link)
    soup = BeautifulSoup(response.content, "html.parser")
    
    div = soup.select(".summary")
    name = soup.select_one(".product_title").text
    price = soup.select_one(".price").text
    description = soup.select_one(".woocommerce-product-details__short-description").text
    stock = soup.select_one(".stock").text
    print(name, price, description, stock)
    item = {
        "name": name,
        "price": price,
        "description": description,
        "stock": stock
    }
    items.append(item)

# Kafka Producer
producer = KafkaProducer(bootstrap_servers='localhost:9092', 
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

print("Producing messages to Kafka...")
for item in items:
    try:
        producer.send('DBrainTask', item)
        print(f"Produced: {item}")
        time.sleep(1)
    except KafkaError as e:
        print(f"Failed to produce message: {e}")

producer.flush()
producer.close()

# Small delay to ensure producer has finished
time.sleep(5)

# Kafka Consumer
consumer = KafkaConsumer('DBrainTask', 
                         bootstrap_servers='localhost:9092', 
                         auto_offset_reset='earliest', 
                         consumer_timeout_ms=30000, 
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')))

print("Consuming messages from Kafka...")
try:
    with open('data.json', 'w') as f:
        f.write('[')
        counter=0
        for message in consumer:
            counter+=1
            total_items = len(items)
            raw_value = message.value
            print(f"Raw message: {raw_value}")  # Print raw message for debugging
            if raw_value:  # Ensure the message is not empty
                try:
                    data = raw_value
                    print(f"Consumed: {data}")
                    json.dump(data, f)
                    print(total_items)
                    print(counter)
                    if counter != total_items:
                        f.write(',')
                    f.write('\n')
                except json.JSONDecodeError as e:
                    print(f"Failed to decode message: {e}")
            else:
                print("Received empty message")
        f.write(']')
except Exception as e:
    print(f"Error consuming messages: {e}")
