function updatePrice() {
    const checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
    const basePrice = 19.99;
    const additionalPrice = 3.99 * checkboxes.length;
    const totalPrice = basePrice + additionalPrice;
    const euros = Math.floor(totalPrice);
    const cents = (totalPrice % 1).toFixed(2).substring(2);
    document.getElementById('price').innerText = `Total Price: €${totalPrice.toFixed(2)}`;
    document.getElementById('currency_Profi_Paket').textContent = euros;
    document.getElementById('cent_Profi_Paket').textContent = '.' + cents;
}