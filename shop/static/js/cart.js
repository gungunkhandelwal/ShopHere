// Function to handle both authenticated and anonymous users
function handleCartItemUpdate(productId, action) {
    if (user === 'AnonymousUser') {
        addCookieItem(productId, action);
    } else {
        updateUserOrder(productId, action);
    }
        
}

// Event listener for update-cart buttons
document.querySelectorAll('.update-cart').forEach(btn => {
    btn.addEventListener('click', function () {
        const productId = this.dataset.product;
        const action = this.dataset.action;
        handleCartItemUpdate(productId, action);
    });
});

// For anonymous users
function addCookieItem(productId, action) {
    cart[productId] = cart[productId] || { 'quantity': 0 };

    if (action === 'add') {
        cart[productId]['quantity'] += 1;
    } else if (action === 'remove') {
        cart[productId]['quantity'] -= 1;
        if (cart[productId]['quantity'] <= 0) {
            delete cart[productId];
        }
    }

    document.cookie = `cart=${JSON.stringify(cart)}; domain=; path=/`;
    location.reload();
}

// Function to update user order
function updateUserOrder(productId, action) {
    const url = '/update_item/';
    const requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ productId, action }),
    };

    fetch(url, requestOptions)
        .then(response => response.json())
        .then(() => {
            location.reload();
        })
}
