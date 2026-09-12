/**
 * Tradenza International Private Limited - Main UI & Interaction Controller
 * Handles sticky navigation, responsive menus, modal quote workflows,
 * asynchronous form submissions with API + Local fallback, and WhatsApp automation.
 */

const TRADENZA_CONFIG = {
  company: 'Tradenza International Private Limited',
  phone: '+91 98251 15213',
  whatsappRaw: '919825115213',
  email: 'tradenzainternationalprivateli@gmail.com',
  base: 'India'
};

document.addEventListener('DOMContentLoaded', () => {
  initNavbar();
  initMobileMenu();
  initModals();
  initFormSubmissions();
  initWhatsAppButtons();
  initCategoryQuoteTriggers();
});

// ==========================================
// NAVBAR & SCROLL BEHAVIOR
// ==========================================
function initNavbar() {
  const navbar = document.getElementById('mainNavbar');
  if (!navbar) return;

  const handleScroll = () => {
    if (window.scrollY > 30) {
      navbar.classList.add('navbar-scrolled');
      navbar.classList.remove('navbar-top');
    } else {
      navbar.classList.remove('navbar-scrolled');
      navbar.classList.add('navbar-top');
    }
  };

  window.addEventListener('scroll', handleScroll, { passive: true });
  handleScroll();
}

function initMobileMenu() {
  const toggleBtn = document.getElementById('mobileMenuToggle');
  const mobileMenu = document.getElementById('mobileMenuDrawer');
  const closeBtn = document.getElementById('mobileMenuClose');

  if (!toggleBtn || !mobileMenu) return;

  toggleBtn.addEventListener('click', () => {
    mobileMenu.classList.remove('hidden');
    document.body.classList.add('overflow-hidden');
  });

  const closeMenu = () => {
    mobileMenu.classList.add('hidden');
    document.body.classList.remove('overflow-hidden');
  };

  if (closeBtn) closeBtn.addEventListener('click', closeMenu);
  
  mobileMenu.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', closeMenu);
  });
}

// ==========================================
// MODAL MANAGEMENT
// ==========================================
function initModals() {
  const quoteModal = document.getElementById('quoteModal');
  const successModal = document.getElementById('successModal');
  const openQuoteBtns = document.querySelectorAll('.trigger-quote-modal');
  const closeQuoteBtns = document.querySelectorAll('.close-quote-modal');
  const closeSuccessBtns = document.querySelectorAll('.close-success-modal');

  openQuoteBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const category = btn.dataset.category || '';
      const product = btn.dataset.product || '';
      openQuoteModal(category, product);
    });
  });

  closeQuoteBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      if (quoteModal) quoteModal.classList.add('hidden');
      document.body.classList.remove('overflow-hidden');
    });
  });

  closeSuccessBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      if (successModal) successModal.classList.add('hidden');
      document.body.classList.remove('overflow-hidden');
    });
  });

  // Close modals on backdrop click
  [quoteModal, successModal].forEach(modal => {
    if (modal) {
      modal.addEventListener('click', (e) => {
        if (e.target === modal) {
          modal.classList.add('hidden');
          document.body.classList.remove('overflow-hidden');
        }
      });
    }
  });
}

function openQuoteModal(category = '', product = '') {
  const quoteModal = document.getElementById('quoteModal');
  if (!quoteModal) return;

  const categorySelect = quoteModal.querySelector('#modal_category');
  const productInput = quoteModal.querySelector('#modal_product');

  if (categorySelect && category) {
    categorySelect.value = category;
  }
  if (productInput && product) {
    productInput.value = product;
  }

  quoteModal.classList.remove('hidden');
  document.body.classList.add('overflow-hidden');
}

function showSuccessModal(title, message, whatsappContext = '') {
  const successModal = document.getElementById('successModal');
  if (!successModal) {
    alert(message);
    return;
  }

  const titleEl = successModal.querySelector('#successModalTitle');
  const messageEl = successModal.querySelector('#successModalMessage');
  const waBtn = successModal.querySelector('#successModalWhatsAppBtn');

  if (titleEl) titleEl.innerText = title || "Requirement Received";
  if (messageEl) messageEl.innerText = message || "Thank you. Your requirement has been received. The Tradenza International team will review it and contact you.";

  if (waBtn && whatsappContext) {
    const waUrl = `https://wa.me/${TRADENZA_CONFIG.whatsappRaw}?text=${encodeURIComponent(whatsappContext)}`;
    waBtn.href = waUrl;
    waBtn.classList.remove('hidden');
  }

  successModal.classList.remove('hidden');
  document.body.classList.add('overflow-hidden');
}

// ==========================================
// CATEGORY CARDS "REQUEST A QUOTE" TRIGGERS
// ==========================================
function initCategoryQuoteTriggers() {
  document.querySelectorAll('.category-quote-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const categoryName = btn.dataset.category || '';
      openQuoteModal(categoryName, categoryName);
    });
  });
}

// ==========================================
// FORM SUBMISSIONS (RFQ, Buyer, Supplier, Contact)
// ==========================================
function initFormSubmissions() {
  // 1. Dedicated RFQ Form (Page or Modal)
  const rfqForms = document.querySelectorAll('form[data-form-type="rfq"]');
  rfqForms.forEach(form => {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      await handleFormSubmit(form, '/api/rfq', 'RFQ');
    });
  });

  // 2. Buyer Requirement Form
  const buyerForms = document.querySelectorAll('form[data-form-type="buyer"]');
  buyerForms.forEach(form => {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      await handleFormSubmit(form, '/api/buyer', 'Buyer Requirement');
    });
  });

  // 3. Supplier Registration Form
  const supplierForms = document.querySelectorAll('form[data-form-type="supplier"]');
  supplierForms.forEach(form => {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      await handleFormSubmit(form, '/api/supplier', 'Supplier Application');
    });
  });

  // 4. Contact Form
  const contactForms = document.querySelectorAll('form[data-form-type="contact"]');
  contactForms.forEach(form => {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      await handleFormSubmit(form, '/api/contact', 'Contact Message');
    });
  });
}

async function handleFormSubmit(form, endpoint, formLabel) {
  const submitBtn = form.querySelector('button[type="submit"]');
  const originalBtnHtml = submitBtn ? submitBtn.innerHTML : 'Submit';

  // Extract Form Data
  const formData = new FormData(form);
  const data = {};
  formData.forEach((val, key) => {
    data[key] = val.trim();
  });

  // Disable button & show spinner
  if (submitBtn) {
    submitBtn.disabled = true;
    submitBtn.innerHTML = `
      <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-current inline-block" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
      </svg>
      Processing...
    `;
  }

  // WhatsApp Context message
  const waContext = `Hello Tradenza International, I submitted a ${formLabel}:\n- Name: ${data.name || ''}\n- Company: ${data.company || 'N/A'}\n- Product/Subject: ${data.product || data.products || data.subject || ''}\n- Country: ${data.country || data.destination_country || 'India'}`;

  try {
    const res = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify(data)
    });

    const result = await res.json();

    if (res.ok && result.success) {
      // Close quote modal if open
      const quoteModal = document.getElementById('quoteModal');
      if (quoteModal) quoteModal.classList.add('hidden');

      form.reset();
      showSuccessModal(
        "Submission Received",
        result.message || "Thank you. Your requirement has been received. The Tradenza International team will review it and contact you.",
        waContext
      );
    } else {
      alert(result.message || "Unable to submit requirement. Please check the entered fields.");
    }
  } catch (err) {
    console.warn("Backend API unavailable. Saving to local database fallback.", err);
    // Offline / Standalone Fallback
    saveLocalFallback(formLabel, data);

    const quoteModal = document.getElementById('quoteModal');
    if (quoteModal) quoteModal.classList.add('hidden');

    form.reset();
    showSuccessModal(
      "Requirement Received",
      "Thank you. Your requirement has been received. The Tradenza International team will review it and contact you.",
      waContext
    );
  } finally {
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.innerHTML = originalBtnHtml;
    }
  }
}

// Client-Side Persistence Fallback
function saveLocalFallback(type, data) {
  try {
    const existing = JSON.parse(localStorage.getItem('tradenza_local_leads') || '[]');
    const record = {
      id: Date.now(),
      type: type.toLowerCase(),
      status: 'New',
      created_at: new Date().toISOString(),
      ...data
    };
    existing.unshift(record);
    localStorage.setItem('tradenza_local_leads', JSON.stringify(existing));
  } catch (e) {
    console.error("Local storage error:", e);
  }
}

// ==========================================
// WHATSAPP INTEGRATION HELPERS
// ==========================================
function initWhatsAppButtons() {
  document.querySelectorAll('.btn-whatsapp-direct').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const customMsg = btn.dataset.msg || "Hello Tradenza International, I would like to inquire about global sourcing from India.";
      const url = `https://wa.me/${TRADENZA_CONFIG.whatsappRaw}?text=${encodeURIComponent(customMsg)}`;
      window.open(url, '_blank');
    });
  });
}
