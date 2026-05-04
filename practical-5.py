# Practical 5: Elementary Chatbot for Customer Interaction

SHOP_NAME = "ShopEasy"

SAMPLE_ORDERS = {
    "SE101": {
        "status": "Packed",
        "delivery": "Expected delivery: 4 May 2026",
        "item": "Wireless Mouse",
    },
    "SE102": {
        "status": "Out for delivery",
        "delivery": "Expected delivery: Today",
        "item": "Bluetooth Headphones",
    },
    "SE103": {
        "status": "Delivered",
        "delivery": "Delivered on: 30 April 2026",
        "item": "Laptop Stand",
    },
}


def greet_user():
    print(f"Welcome to {SHOP_NAME} Customer Support!")
    print("I am your virtual assistant. How can I help you today?")
    print("Type 'help' to see options or 'bye' to exit.")
    print("Sample order IDs for testing: SE101, SE102, SE103\n")


def show_help():
    print("\nYou can ask me about:")
    print("1. order status")
    print("2. return or refund")
    print("3. payment")
    print("4. delivery")
    print("5. contact support")
    print("6. offers")
    print("7. complaint")
    print("8. store timings")
    print("\nExample: 'track SE102' or 'I want a refund'")


def track_order(order_id):
    order_id = order_id.upper()
    order = SAMPLE_ORDERS.get(order_id)

    if not order:
        return (
            "I could not find that order ID. "
            "Please check the ID and try again. Example: SE102"
        )

    return (
        f"Order {order_id} - {order['item']}\n"
        f"Status: {order['status']}\n"
        f"{order['delivery']}"
    )


def find_order_id(words):
    for word in words:
        cleaned_word = word.strip(".,!?;:").upper()
        if cleaned_word.startswith("SE") and cleaned_word[2:].isdigit():
            return cleaned_word
    return None


def calculate_delivery_charge(amount):
    if amount >= 500:
        return "Delivery is free for this order."
    return "Delivery charge is Rs. 40. Add items worth Rs. 500 or more for free delivery."


def create_complaint_ticket(order_id):
    if not order_id:
        return (
            "Please share your order ID so I can create a complaint ticket. "
            "Example: damaged product SE103"
        )

    if order_id not in SAMPLE_ORDERS:
        return "I could not create a ticket because this order ID was not found."

    ticket_number = "TKT-" + order_id
    return (
        f"Complaint registered successfully.\n"
        f"Ticket number: {ticket_number}\n"
        "Our support team will contact you within 24 hours."
    )


def get_bot_response(user_input):
    message = user_input.lower()
    words = user_input.split()
    order_id = find_order_id(words)

    if "help" in message or "option" in message:
        return "HELP"

    if "order" in message or "track" in message or "status" in message:
        if order_id:
            return track_order(order_id)
        return (
            "Please enter your order ID to track it. "
            "Example: track SE102"
        )

    if "return" in message or "refund" in message or "replace" in message:
        return (
            "Return/refund policy:\n"
            "- Return window: 7 days after delivery\n"
            "- Product should be unused and in original packaging\n"
            "- Refund is processed within 3-5 working days after pickup\n"
            "To begin, type your order ID with the issue. Example: refund SE103"
        )

    if "payment" in message or "paid" in message or "card" in message or "upi" in message:
        return (
            "We support UPI, debit card, credit card, net banking, and cash on delivery. "
            "If payment failed but money was deducted, it is usually refunded within 3-5 working days."
        )

    if "delivery" in message or "shipping" in message or "late" in message:
        if order_id:
            return track_order(order_id)
        return (
            "Standard delivery takes 3-5 working days. "
            "Orders above Rs. 500 get free delivery. "
            "For delayed delivery, type your order ID. Example: delivery SE101"
        )

    if "contact" in message or "support" in message or "agent" in message:
        return (
            "You can contact our customer care at support@shopeasy.com "
            "or call 1800-123-456 between 9 AM and 8 PM."
        )

    if "offer" in message or "discount" in message or "coupon" in message:
        return (
            "Today's offers are available in the 'Deals' section. "
            "You can apply valid coupon codes during checkout."
        )

    if "complaint" in message or "problem" in message or "damaged" in message:
        return create_complaint_ticket(order_id)

    if "time" in message or "timing" in message or "open" in message:
        return "Our support team is available every day from 9 AM to 8 PM."

    if "charge" in message or "fee" in message:
        for word in words:
            if word.isdigit():
                return calculate_delivery_charge(int(word))
        return "Please enter your cart amount to calculate delivery charge. Example: charge 450"

    if "thank" in message:
        return "You are welcome! Is there anything else I can help you with?"

    return (
        "Sorry, I did not understand that. "
        "Please type 'help' to see what I can assist you with."
    )


def start_chatbot():
    greet_user()

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            print("Bot: Please enter a message.")
            continue

        if user_input.lower() in ["bye", "exit", "quit"]:
            print("Bot: Thank you for contacting ShopEasy. Have a great day!")
            break

        response = get_bot_response(user_input)

        if response == "HELP":
            show_help()
        else:
            print("Bot:", response)

if __name__ == "__main__":
    start_chatbot()