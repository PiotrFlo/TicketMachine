import json
import re

with open("prices.json", "r", encoding="UTF-8") as file:
    prices = json.load(file)


def display_menu(menu):
    print("Jaką opcję biletu chcesz kupić?")
    options = list(menu.keys())
    for index, option in enumerate(options):
        print(f"{index} - {option}")
    try:
        choice = int(input("Wybór: "))
    except ValueError:
        print("Wprowaadzono niepoprawny typ wartości. ")
        return display_menu(menu)
    if choice > len(options) - 1 or choice < 0:
        raise ValueError("Wprowadzono błędny numer opcji.")
        return display_menu(menu)
    menu = menu[options[choice]]
    if isinstance(menu, dict):
        return display_menu(menu)
    else:
        return options[choice], menu


def register_payment(cart):
    total = sum(price for _, price in cart)
    print(f"Kwota do zapłaty - {total}")
    payment_method = input("Wybierz metodę płatności: \nb - BLIK\nk - karta\ng - gotówka ")
    if payment_method == "b":
        blik = input("Podaj kod BLIK: ")
        if re.search(r"^[0-9]{6}$", blik):
            print("Transakcja się powiodła")
        else:
            decision = input("Wprowadzono niepoprawny kod. Czy chcesz sprobować jeszcze raz (t/n)? ")
            if decision.lower() == "t":
                register_payment(cart)
            else:
                exit()
    elif payment_method == "k":
        print("Proszę zbliżyć kartę do czytnika...")
        input("Podtwierdz transakcje: ")
        print("Transakcja się powiodła")
    elif payment_method == "g":
        paid = 0
        while paid < total:
            try:
                paid += float(input("Wprowadż gotówkę: "))
            except ValueError:
                paid += 0
            if paid < total:
                decision = input("Wprowadzono za mało gotówki. Czy chcesz dopłacić (t/n)? ")
                if decision.lower() == "t":
                    continue
                else:
                    exit()
        if paid >= total:
            print(f"Reszta: {paid - total} zł")
    else:
        decision = input("Wybrano niepoprawną opcję. Czy chcesz sprobować jeszcze raz (t/n)? ")
        if decision.lower() == "t":
            register_payment(cart)
        else:
            exit()


def display_cart(cart):
    for ticket, price in cart:
        print(f"{ticket}\t{price}zł")


cart = []
add_another = "t"
while add_another.lower() == "t":
    cart.append(display_menu(prices))
    add_another = input("Czy chcesz dodać kolejny bilet (t/n)?")
register_payment(cart)
input("Drukowanie biletów. Proszę czekać...")
display_cart(cart)
print("Dziękujemy za skorzystanie z automatu biletowego. Zapraszamy ponownie")