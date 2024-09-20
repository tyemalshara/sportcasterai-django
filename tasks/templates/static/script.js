document.addEventListener("DOMContentLoaded", function() {
document.getElementById('apply-button').addEventListener('click', function() {
    const basePrice = 19.99;
    const sportPrice = 3.99;
    const sportsCheckboxes = document.querySelectorAll('#sports input[type="checkbox"]');
    const selectedSports = Array.from(sportsCheckboxes)
                                .filter(checkbox => checkbox.checked)
                                .map(checkbox => checkbox.value);

    const newPrice = basePrice + (selectedSports.length * sportPrice);
    const priceTag = document.querySelector('.generic_price_tag .price');

    const dollars = Math.floor(newPrice);
    const cents = (newPrice % 1).toFixed(2).substring(2);

    priceTag.querySelector('.currency').textContent = dollars;
    priceTag.querySelector('.cent').textContent = '.' + cents;
    priceTag.querySelector('.sign').textContent = '€';
    priceTag.querySelector('.month').textContent = '/MON';

    document.getElementById('selected-sports').textContent = 'Selected sports: ' + (selectedSports.length > 0 ? selectedSports.join(', ') : 'None');
});
});