(async function initProductDetail() {
    const data = await getProductDetailData();
    if (!data) return;

    const urlParams = new URLSearchParams(window.location.search);
    const productId = urlParams.get('id');
    const product = data.products?.[productId];

    if (!product) {
        document.body.innerHTML = `<h1 style="text-align: center; padding-top: 100px;">${escapeHtml(data.messages?.notFound || 'Producto no encontrado')}</h1>`;
        return;
    }

    const productName = document.getElementById('productName');
    const productDesc = document.getElementById('productDesc');
    const productPrice = document.getElementById('productPrice');
    const productImage = document.getElementById('productImage');
    const colorOptions = document.getElementById('colorOptions');
    const sizeGroup = document.getElementById('sizeGroup');
    const sizeSelector = document.getElementById('sizeSelector');
    const sizeError = document.getElementById('sizeError');
    const quantityInput = document.getElementById('quantity');
    const addToCartBtn = document.getElementById('addToCartBtn');
    const confirmationMessage = document.getElementById('confirmationMessage');

    productName.textContent = product.name;
    productDesc.textContent = product.description;
    productPrice.textContent = product.price;
    productImage.src = product.colors[0].image;
    confirmationMessage.textContent = data.messages?.added || '✓ Producto agregado al carrito';
    sizeError.textContent = data.messages?.sizeRequired || 'Por favor selecciona una talla';

    product.colors.forEach((color, index) => {
        const colorBtn = document.createElement('button');
        colorBtn.className = 'color-btn' + (index === 0 ? ' active' : '');
        colorBtn.type = 'button';
        colorBtn.style.backgroundColor = color.hex;
        colorBtn.title = color.name;
        colorBtn.addEventListener('click', () => {
            document.querySelectorAll('.color-btn').forEach((btn) => btn.classList.remove('active'));
            colorBtn.classList.add('active');
            productImage.src = color.image;
        });
        colorOptions.appendChild(colorBtn);
    });

    if (product.hasSize) {
        sizeGroup.style.display = 'block';
    }

    document.getElementById('decreaseQty').addEventListener('click', () => {
        if (quantityInput.value > 1) quantityInput.value = String(Number(quantityInput.value) - 1);
    });

    document.getElementById('increaseQty').addEventListener('click', () => {
        if (quantityInput.value < 10) quantityInput.value = String(Number(quantityInput.value) + 1);
    });

    addToCartBtn.addEventListener('click', () => {
        const activeColorBtn = document.querySelector('.color-btn.active');
        const color = activeColorBtn?.title || product.colors[0].name;
        const selectedColor = product.colors.find((c) => c.name === color) || product.colors[0];
        const size = product.hasSize ? sizeSelector.value : 'Unica';
        const quantity = Number(quantityInput.value);

        if (product.hasSize && !size) {
            sizeError.style.display = 'flex';
            setTimeout(() => {
                sizeError.style.display = 'none';
            }, 3000);
            return;
        }

        const cart = JSON.parse(localStorage.getItem('cart')) || [];
        cart.push({
            id: productId,
            name: product.name,
            price: product.price,
            color,
            image: selectedColor.image,
            size,
            quantity
        });
        localStorage.setItem('cart', JSON.stringify(cart));

        updateCartCount();
        addToCartBtn.style.display = 'none';
        confirmationMessage.style.display = 'block';

        setTimeout(() => {
            addToCartBtn.style.display = 'block';
            confirmationMessage.style.display = 'none';
            quantityInput.value = '1';
            if (product.hasSize) {
                sizeSelector.value = '';
            }
        }, 2000);
    });

    updateCartCount();
})();

async function getProductDetailData() {
    if (window.PRODUCT_DETAIL_DATA && Object.keys(window.PRODUCT_DETAIL_DATA).length > 0) {
        return window.PRODUCT_DETAIL_DATA;
    }

    try {
        const response = await fetch('product-detail-data.json', { cache: 'no-store' });
        if (!response.ok) {
            throw new Error(`No se pudo cargar product-detail-data.json (${response.status})`);
        }
        return response.json();
    } catch (error) {
        console.error('Error al cargar product-detail-data:', error);
        return null;
    }
}

function updateCartCount() {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    const cartCount = document.getElementById('cartCount');
    if (cartCount) {
        cartCount.textContent = cart.length;
    }
}

function escapeHtml(value) {
    return String(value ?? '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/\"/g, '&quot;')
        .replace(/'/g, '&#39;');
}
