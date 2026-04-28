async function loadMerchPage() {
    try {
        const data = await getMerchData();
        renderMerchProducts(data);
        bindMerchEvents();
        updateCartCount();
    } catch (error) {
        console.error('Error al cargar merchandising:', error);
    }
}

async function getMerchData() {
    if (window.MERCH_DATA) {
        return window.MERCH_DATA;
    }

    const response = await fetch('merch-data.json', { cache: 'no-store' });
    if (!response.ok) {
        throw new Error(`No se pudo cargar merch-data.json (${response.status})`);
    }

    return response.json();
}

function renderMerchProducts(data) {
    const categories = data?.categories || [];

    categories.forEach((category) => {
        const grid = document.getElementById(`${category.id}Grid`);

        if (!grid) {
            return;
        }

        grid.innerHTML = (category.products || [])
            .map((product) => buildProductHtml(product, category.id))
            .join('');
    });
}

function buildProductHtml(product, categoryId) {
    const isLimited = categoryId === 'edicion-limitada';
    const premiumClass = isLimited ? ' premium' : '';
    const badgeHtml = isLimited ? '<div class="limited-badge">LIMITADA</div>' : '';
    const limitedHtml = Number.isInteger(product.limitedUnits)
        ? `<p class="merch-limited">Solo quedan: <strong>${product.limitedUnits} unidades</strong></p>`
        : '';

    const colorsHtml = Array.isArray(product.colors) && product.colors.length > 1
        ? `
            <div class="merch-colors">
                ${product.colors.map((color) => {
                    const borderStyle = color.border ? ` border: ${escapeHtml(color.border)};` : '';
                    return `<span class="color" data-image="${escapeHtml(color.image)}" style="background-color: ${escapeHtml(color.hex)};${borderStyle}" title="${escapeHtml(color.name)}"></span>`;
                }).join('')}
            </div>
        `
        : '';

    return `
        <div class="merch-card${premiumClass}" data-product-id="${product.id}" style="cursor: pointer;" data-link="product-detail.html?id=${product.id}">
            ${badgeHtml}
            <div class="merch-image" style="background-image: url('${escapeHtml(product.defaultImage)}');"></div>
            <div class="merch-body">
                <h3>${escapeHtml(product.name)}</h3>
                <p class="merch-desc">${escapeHtml(product.description)}</p>
                ${colorsHtml}
                ${limitedHtml}
                <p class="merch-price">${escapeHtml(product.price)}</p>
            </div>
        </div>
    `;
}

function bindMerchEvents() {
    document.querySelectorAll('.merch-card').forEach((card) => {
        card.addEventListener('click', () => {
            const link = card.dataset.link;
            if (link) {
                window.location.href = link;
            }
        });
    });

    document.querySelectorAll('.color').forEach((colorSpan) => {
        colorSpan.addEventListener('click', (event) => {
            event.stopPropagation();

            const productCard = colorSpan.closest('.merch-card');
            const merchImage = productCard?.querySelector('.merch-image');
            const image = colorSpan.dataset.image;

            if (merchImage && image) {
                merchImage.style.backgroundImage = `url('${image}')`;
            }
        });
    });

    window.addEventListener('storage', updateCartCount);
    setInterval(updateCartCount, 500);
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

document.addEventListener('DOMContentLoaded', loadMerchPage);
