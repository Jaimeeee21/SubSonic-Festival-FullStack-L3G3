let cartViewData = window.CART_DATA || null;

(async function initCartView() {
    if (!cartViewData) {
        try {
            const response = await fetch('cart-data.json', { cache: 'no-store' });
            if (response.ok) {
                cartViewData = await response.json();
            }
        } catch (error) {
            console.error('Error al cargar cart-data:', error);
        }
    }

    loadCartPage();

    window.addEventListener('click', (event) => {
        const modal = document.getElementById('clearCartModal');
        if (event.target === modal) {
            closeClearCartModal();
        }
    });
})();

function loadCartPage() {
    const labels = cartViewData?.labels || {};
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    const cartPageItemsContainer = document.getElementById('cartPageItems');
    const summary = document.querySelector('.cart-page-summary');

    if (cart.length === 0) {
        cartPageItemsContainer.innerHTML = `<p style="text-align: center; padding: 3rem; color: rgba(255,255,255,0.6); font-size: 1.1rem;">${escapeHtml(labels.emptyCart || 'Tu carrito esta vacio')}</p>`;
        if (summary) summary.style.display = 'none';
        return;
    }

    if (summary) summary.style.display = 'block';
    cartPageItemsContainer.innerHTML = '';

    cart.forEach((item, index) => {
        const price = Number(String(item.price).replace('$', ''));
        const itemTotal = price * Number(item.quantity);
        const singleSize = labels.singleSize || 'Unica';
        const sizePrefix = labels.sizePrefix || '- Talla:';

        const cartPageItem = document.createElement('div');
        cartPageItem.className = 'cart-page-item';
        cartPageItem.innerHTML = `
            <div class="cart-page-item-image" style="background-image: url('${escapeHtml(item.image)}');"></div>
            <div class="cart-page-item-details">
                <h3>${escapeHtml(item.name)}</h3>
                <p class="item-variant">${escapeHtml(item.color)} ${item.size !== singleSize ? `${escapeHtml(sizePrefix)} ${escapeHtml(item.size)}` : ''}</p>
                <p class="item-price">${escapeHtml(labels.itemPricePrefix || 'Precio:')} <span style="color: #00d4ff; font-weight: 600;">${escapeHtml(item.price)}</span></p>
            </div>
            <div class="cart-page-item-quantity">
                <button class="qty-btn" onclick="decreaseQuantity(${index})">−</button>
                <input type="number" value="${Number(item.quantity)}" min="1" readonly>
                <button class="qty-btn" onclick="increaseQuantity(${index})">+</button>
            </div>
            <div class="cart-page-item-total">
                <p class="item-total">$${itemTotal.toFixed(2)}</p>
            </div>
            <button class="cart-item-delete" onclick="removeFromCart(${index})">🗑️</button>
        `;
        cartPageItemsContainer.appendChild(cartPageItem);
    });

    updateCartSummary();
}

function updateCartSummary() {
    const labels = cartViewData?.labels || {};
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    let subtotal = 0;

    cart.forEach((item) => {
        const price = Number(String(item.price).replace('$', ''));
        subtotal += price * Number(item.quantity);
    });

    const shipping = subtotal > 100 ? 0 : 10;
    const tax = subtotal * 0.1;
    const total = subtotal + shipping + tax;

    document.getElementById('subtotal').textContent = '$' + subtotal.toFixed(2);
    document.getElementById('shipping').textContent = shipping === 0 ? (labels.freeShipping || 'GRATIS') : '$' + shipping.toFixed(2);
    document.getElementById('tax').textContent = '$' + tax.toFixed(2);
    document.getElementById('totalPrice').textContent = '$' + total.toFixed(2);
}

function increaseQuantity(index) {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    if (cart[index] && Number(cart[index].quantity) < 10) {
        cart[index].quantity = Number(cart[index].quantity) + 1;
        localStorage.setItem('cart', JSON.stringify(cart));
        loadCartPage();
    }
}

function decreaseQuantity(index) {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    if (cart[index] && Number(cart[index].quantity) > 1) {
        cart[index].quantity = Number(cart[index].quantity) - 1;
        localStorage.setItem('cart', JSON.stringify(cart));
        loadCartPage();
    }
}

function removeFromCart(index) {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    cart.splice(index, 1);
    localStorage.setItem('cart', JSON.stringify(cart));
    loadCartPage();
}

function openClearCartModal() {
    document.getElementById('clearCartModal').style.display = 'flex';
}

function closeClearCartModal() {
    document.getElementById('clearCartModal').style.display = 'none';
}

function confirmClearCart() {
    localStorage.setItem('cart', JSON.stringify([]));
    closeClearCartModal();
    loadCartPage();
}

function proceedToCheckout() {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    const labels = cartViewData?.labels || {};

    if (cart.length === 0) {
        alert(labels.emptyCheckout || 'Tu carrito esta vacio');
        return;
    }

    window.location.href = cartViewData?.checkoutUrl || 'checkout.html';
}

function escapeHtml(value) {
    return String(value ?? '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/\"/g, '&quot;')
        .replace(/'/g, '&#39;');
}
