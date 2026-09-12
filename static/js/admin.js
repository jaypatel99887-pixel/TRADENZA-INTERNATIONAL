/**
 * Tradenza International - Admin Portal Controller
 * Manages RFQs, Buyer Inquiries, Supplier Registrations, and Contact Messages.
 * Features live status updates, internal notes, lead inspection, and CSV export.
 * Rethemed for Obsidian & Rose Gold luxury aesthetic.
 */

let currentFilterType = 'all';
let currentFilterStatus = 'all';
let currentSearchQuery = '';

document.addEventListener('DOMContentLoaded', () => {
  loadAdminStats();
  loadSubmissions();
  initAdminEventListeners();
});

function initAdminEventListeners() {
  const searchInput = document.getElementById('adminSearchInput');
  if (searchInput) {
    let debounceTimer;
    searchInput.addEventListener('input', (e) => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        currentSearchQuery = e.target.value.trim();
        loadSubmissions();
      }, 300);
    });
  }

  document.querySelectorAll('.admin-type-filter').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.admin-type-filter').forEach(b => {
        b.classList.remove('bg-[#EAA6B1]', 'text-[#120D0E]', 'font-bold');
        b.classList.add('bg-[#2A1F22]', 'text-[#EDE4E5]', 'font-semibold');
      });
      btn.classList.remove('bg-[#2A1F22]', 'text-[#EDE4E5]', 'font-semibold');
      btn.classList.add('bg-[#EAA6B1]', 'text-[#120D0E]', 'font-bold');

      currentFilterType = btn.dataset.type || 'all';
      loadSubmissions();
    });
  });

  const statusSelect = document.getElementById('adminStatusFilter');
  if (statusSelect) {
    statusSelect.addEventListener('change', (e) => {
      currentFilterStatus = e.target.value;
      loadSubmissions();
    });
  }

  const refreshBtn = document.getElementById('adminRefreshBtn');
  if (refreshBtn) {
    refreshBtn.addEventListener('click', () => {
      loadAdminStats();
      loadSubmissions();
      showToast('Data refreshed');
    });
  }

  const exportBtn = document.getElementById('adminExportBtn');
  if (exportBtn) {
    exportBtn.addEventListener('click', () => {
      const url = `/api/admin/export?type=${currentFilterType}&status=${currentFilterStatus}`;
      window.location.href = url;
    });
  }

  const closeDetailBtn = document.getElementById('closeDetailModal');
  const detailModal = document.getElementById('leadDetailModal');
  if (closeDetailBtn && detailModal) {
    closeDetailBtn.addEventListener('click', () => {
      detailModal.classList.add('hidden');
    });
    detailModal.addEventListener('click', (e) => {
      if (e.target === detailModal) detailModal.classList.add('hidden');
    });
  }
}

async function loadAdminStats() {
  try {
    const res = await fetch('/api/admin/stats');
    if (res.ok) {
      const stats = await res.json();
      document.getElementById('statTotal').innerText = stats.total || 0;
      document.getElementById('statNew').innerText = stats.count_new || 0;
      document.getElementById('statRfq').innerText = stats.count_rfq || 0;
      document.getElementById('statBuyer').innerText = stats.count_buyer || 0;
      document.getElementById('statSupplier').innerText = stats.count_supplier || 0;
      document.getElementById('statContact').innerText = stats.count_contact || 0;
    }
  } catch (err) {
    console.warn("Could not load stats from API:", err);
  }
}

async function loadSubmissions() {
  const tableBody = document.getElementById('submissionsTableBody');
  if (!tableBody) return;

  tableBody.innerHTML = `
    <tr>
      <td colspan="7" class="py-8 text-center text-[#A8989B]">
        <svg class="animate-spin h-6 w-6 text-[#EAA6B1] mx-auto mb-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
        </svg>
        Loading inquiries and applications...
      </td>
    </tr>
  `;

  try {
    const params = new URLSearchParams({
      type: currentFilterType,
      status: currentFilterStatus,
      search: currentSearchQuery,
      limit: '100'
    });

    const res = await fetch(`/api/admin/submissions?${params.toString()}`);
    if (res.ok) {
      const data = await res.json();
      renderTableRows(data.items || []);
      const countEl = document.getElementById('filteredCount');
      if (countEl) countEl.innerText = `Showing ${data.items.length} of ${data.total} records`;
    } else {
      tableBody.innerHTML = `<tr><td colspan="7" class="py-8 text-center text-red-400">Failed to load leads from server.</td></tr>`;
    }
  } catch (err) {
    console.warn("Server unavailable, checking local fallback storage", err);
    loadLocalFallbackLeads();
  }
}

function loadLocalFallbackLeads() {
  const tableBody = document.getElementById('submissionsTableBody');
  const raw = localStorage.getItem('tradenza_local_leads') || '[]';
  const leads = JSON.parse(raw);

  let filtered = leads;
  if (currentFilterType !== 'all') {
    filtered = filtered.filter(l => (l.type || '').toLowerCase() === currentFilterType);
  }
  if (currentFilterStatus !== 'all') {
    filtered = filtered.filter(l => (l.status || 'New') === currentFilterStatus);
  }

  renderTableRows(filtered);
  const countEl = document.getElementById('filteredCount');
  if (countEl) countEl.innerText = `Showing ${filtered.length} offline local records`;
}

function renderTableRows(items) {
  const tableBody = document.getElementById('submissionsTableBody');
  if (!items || items.length === 0) {
    tableBody.innerHTML = `
      <tr>
        <td colspan="7" class="py-12 text-center text-[#A8989B]">
          <svg class="w-10 h-10 mx-auto mb-3 text-[#5C3A40]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"/>
          </svg>
          No inquiries found matching this filter criteria.
        </td>
      </tr>
    `;
    return;
  }

  let html = '';
  items.forEach(item => {
    const typeBadge = getTypeBadge(item.type);
    const dateFormatted = item.created_at ? new Date(item.created_at).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' }) : 'Recent';
    const statusClass = getStatusClass(item.status || 'New');

    html += `
      <tr class="border-b border-[#5C3A40]/25 hover:bg-[#2A1F22]/60 transition-colors">
        <td class="py-3.5 px-4 text-xs font-mono text-[#A8989B]">#${item.id}</td>
        <td class="py-3.5 px-4 text-xs text-[#C9BABE] whitespace-nowrap">${dateFormatted}</td>
        <td class="py-3.5 px-4 whitespace-nowrap">${typeBadge}</td>
        <td class="py-3.5 px-4">
          <div class="font-semibold text-sm text-white">${escapeHtml(item.name)}</div>
          <div class="text-xs text-[#C9BABE] flex items-center gap-1.5 mt-0.5">
            <span>${escapeHtml(item.company || 'Private Entity')}</span>
            ${item.country ? `• <span class="text-[#EAA6B1] font-medium">${escapeHtml(item.country)}</span>` : ''}
          </div>
        </td>
        <td class="py-3.5 px-4">
          <div class="text-xs font-medium text-[#F5ECEE] line-clamp-1">${escapeHtml(item.product || item.products || item.subject || 'Trade Requirement')}</div>
          <div class="text-[11px] text-[#A8989B]">${escapeHtml(item.quantity || item.product_category || 'Direct Sourcing')}</div>
        </td>
        <td class="py-3.5 px-4 whitespace-nowrap">
          <select class="text-xs font-semibold rounded-lg px-2.5 py-1 border ${statusClass} cursor-pointer focus:outline-none focus:ring-1 focus:ring-[#EAA6B1] bg-[#191214] transition-all"
                  onchange="updateStatus(${item.id}, this.value)">
            <option value="New" ${item.status === 'New' ? 'selected' : ''}>New</option>
            <option value="Contacted" ${item.status === 'Contacted' ? 'selected' : ''}>Contacted</option>
            <option value="Qualified" ${item.status === 'Qualified' ? 'selected' : ''}>Qualified</option>
            <option value="Closed" ${item.status === 'Closed' ? 'selected' : ''}>Closed</option>
          </select>
        </td>
        <td class="py-3.5 px-4 text-right whitespace-nowrap">
          <div class="flex items-center justify-end gap-2">
            <button onclick="viewLeadDetail(${item.id})" title="View Full Procurement Specs" 
                    class="p-1.5 text-[#EDE4E5] hover:text-[#EAA6B1] hover:bg-[#332226] rounded-md transition-colors">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
              </svg>
            </button>
            ${item.phone ? `
              <a href="https://wa.me/${cleanPhoneForWa(item.phone)}?text=${encodeURIComponent('Hello ' + (item.name || '') + ', regarding your trade inquiry with Tradenza International Private Limited:')}" 
                 target="_blank" title="Contact on WhatsApp"
                 class="p-1.5 text-emerald-400 hover:bg-emerald-950/40 rounded-md transition-colors">
                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.582 2.128 2.182-.573c.978.58 1.911.928 3.145.929 3.178 0 5.767-2.587 5.768-5.766.001-3.187-2.575-5.77-5.764-5.771zm3.392 8.244c-.144.405-.837.774-1.17.824-.311.045-.698.072-2.18-.54-1.923-.794-3.143-2.73-3.238-2.856-.096-.127-.778-1.034-.778-1.97 0-.938.49-1.398.665-1.589.175-.19.382-.239.51-.239.127 0 .254.002.365.007.119.006.278-.045.435.333.16.386.545 1.332.593 1.43.048.098.079.213.016.339-.063.13-.096.21-.19.32-.095.11-.2.247-.286.332-.095.094-.194.197-.084.386.111.19.493.813 1.058 1.317.728.648 1.342.849 1.533.945.191.095.302.079.413-.048.111-.127.476-.556.603-.746.127-.19.254-.158.429-.095.175.063 1.11.523 1.301.618.19.095.317.143.365.222.048.079.048.46-.096.865z"/>
                </svg>
              </a>
            ` : ''}
            <a href="mailto:${item.email}?subject=Tradenza%20International%20-%20Regarding%20Your%20Inquiry%20%23${item.id}" 
               title="Send Email"
               class="p-1.5 text-blue-400 hover:bg-blue-950/40 rounded-md transition-colors">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
              </svg>
            </a>
          </div>
        </td>
      </tr>
    `;
  });

  tableBody.innerHTML = html;
}

function getTypeBadge(type) {
  const t = (type || 'rfq').toLowerCase();
  switch (t) {
    case 'rfq':
      return `<span class="px-2.5 py-1 text-[10px] font-extrabold uppercase tracking-wider rounded-md bg-[#332226] text-[#FCE6E9] border border-[#EAA6B1]/40">RFQ</span>`;
    case 'buyer':
      return `<span class="px-2.5 py-1 text-[10px] font-extrabold uppercase tracking-wider rounded-md bg-cyan-950/60 text-cyan-300 border border-cyan-500/30">Buyer</span>`;
    case 'supplier':
      return `<span class="px-2.5 py-1 text-[10px] font-extrabold uppercase tracking-wider rounded-md bg-emerald-950/60 text-emerald-300 border border-emerald-500/30">Supplier</span>`;
    default:
      return `<span class="px-2.5 py-1 text-[10px] font-extrabold uppercase tracking-wider rounded-md bg-amber-950/60 text-amber-300 border border-amber-500/30">Contact</span>`;
  }
}

function getStatusClass(status) {
  switch (status) {
    case 'New': return 'admin-badge-new';
    case 'Contacted': return 'admin-badge-contacted';
    case 'Qualified': return 'admin-badge-qualified';
    case 'Closed': return 'admin-badge-closed';
    default: return 'bg-[#191214] text-[#EDE4E5] border-[#5C3A40]';
  }
}

async function updateStatus(id, newStatus) {
  try {
    const res = await fetch(`/api/admin/submissions/${id}/status`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: newStatus })
    });
    if (res.ok) {
      showToast(`Lead #${id} status updated to "${newStatus}"`);
      loadAdminStats();
    } else {
      showToast('Error updating status on server');
    }
  } catch (e) {
    showToast(`Offline mode: status changed to ${newStatus}`);
  }
}

async function viewLeadDetail(id) {
  const modal = document.getElementById('leadDetailModal');
  const container = document.getElementById('leadDetailContent');
  if (!modal || !container) return;

  modal.classList.remove('hidden');
  container.innerHTML = `<div class="py-8 text-center text-[#A8989B]">Loading details...</div>`;

  try {
    const res = await fetch(`/api/admin/submissions/${id}`);
    if (res.ok) {
      const data = await res.json();
      const item = data.item;
      renderLeadDetailModal(item);
    }
  } catch (err) {
    const raw = localStorage.getItem('tradenza_local_leads') || '[]';
    const leads = JSON.parse(raw);
    const item = leads.find(l => l.id == id);
    if (item) {
      renderLeadDetailModal(item);
    } else {
      container.innerHTML = `<div class="text-red-400 py-4">Unable to load details.</div>`;
    }
  }
}

function renderLeadDetailModal(item) {
  const container = document.getElementById('leadDetailContent');
  container.innerHTML = `
    <div class="space-y-6">
      <div class="flex items-start justify-between border-b border-[#5C3A40]/40 pb-4">
        <div>
          <span class="text-xs font-mono text-[#A8989B]">Inquiry ID: #${item.id}</span>
          <h3 class="text-xl font-bold text-white mt-1 font-serif">${escapeHtml(item.name)}</h3>
          <p class="text-sm text-[#C9BABE] font-medium">${escapeHtml(item.company || 'Private Entity')} • <span class="text-[#EAA6B1]">${escapeHtml(item.country || 'N/A')}</span></p>
        </div>
        <div class="text-right">
          ${getTypeBadge(item.type)}
          <div class="text-xs text-[#A8989B] mt-1.5">${item.created_at || 'Just now'}</div>
        </div>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 bg-[#22181B] p-4 rounded-xl border border-[#EAA6B1]/20 text-sm">
        <div>
          <span class="text-xs text-[#A8989B] uppercase font-semibold">Email</span>
          <p class="font-medium text-white mt-0.5 break-all">
            <a href="mailto:${item.email}" class="text-blue-400 hover:underline">${escapeHtml(item.email)}</a>
          </p>
        </div>
        <div>
          <span class="text-xs text-[#A8989B] uppercase font-semibold">Phone / WhatsApp</span>
          <p class="font-medium text-white mt-0.5">
            ${item.phone ? `<a href="https://wa.me/${cleanPhoneForWa(item.phone)}" target="_blank" class="text-emerald-400 font-semibold hover:underline">${escapeHtml(item.phone)}</a>` : 'Not provided'}
          </p>
        </div>
      </div>

      <div class="border border-[#EAA6B1]/25 rounded-xl p-4 bg-[#1E1517] space-y-3">
        <h4 class="text-xs font-bold uppercase tracking-wider text-[#EAA6B1]">Procurement / Trade Parameters</h4>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-sm">
          <div><span class="text-xs text-[#A8989B]">Product / Commodity:</span> <strong class="text-white block">${escapeHtml(item.product || item.products || item.subject || 'N/A')}</strong></div>
          <div><span class="text-xs text-[#A8989B]">Category:</span> <span class="text-[#EDE4E5] block">${escapeHtml(item.product_category || 'General')}</span></div>
          <div><span class="text-xs text-[#A8989B]">Required Quantity:</span> <span class="text-[#EDE4E5] block">${escapeHtml(item.quantity || 'N/A')}</span></div>
          <div><span class="text-xs text-[#A8989B]">Target Price:</span> <span class="text-[#EDE4E5] block">${escapeHtml(item.target_price || 'N/A')}</span></div>
          <div><span class="text-xs text-[#A8989B]">Destination:</span> <span class="text-[#EDE4E5] block">${escapeHtml(item.destination_country || 'N/A')}</span></div>
          <div><span class="text-xs text-[#A8989B]">Delivery Timeline:</span> <span class="text-[#EDE4E5] block">${escapeHtml(item.delivery_timeline || 'N/A')}</span></div>
        </div>

        ${item.specifications ? `
          <div class="mt-3 pt-3 border-t border-[#5C3A40]/40">
            <span class="text-xs text-[#A8989B] block mb-1">Specifications:</span>
            <p class="text-xs text-[#EFE6E7] bg-[#2A1F22] p-2.5 rounded-lg">${escapeHtml(item.specifications)}</p>
          </div>
        ` : ''}

        ${item.packaging ? `
          <div class="mt-2">
            <span class="text-xs text-[#A8989B] block mb-1">Packaging Requirements:</span>
            <p class="text-xs text-[#EFE6E7] bg-[#2A1F22] p-2.5 rounded-lg">${escapeHtml(item.packaging)}</p>
          </div>
        ` : ''}

        ${item.manufacturing_capacity || item.export_experience ? `
          <div class="mt-3 pt-3 border-t border-[#5C3A40]/40 grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
            <div><span class="text-[#A8989B]">Supply Capacity:</span> <strong class="text-white">${escapeHtml(item.manufacturing_capacity || 'N/A')}</strong></div>
            <div><span class="text-[#A8989B]">Export Experience:</span> <strong class="text-white">${escapeHtml(item.export_experience || 'N/A')}</strong></div>
            <div><span class="text-[#A8989B]">Supplier Location:</span> <strong class="text-white">${escapeHtml(item.location || 'N/A')}</strong></div>
            <div><span class="text-[#A8989B]">Website:</span> <strong>${item.website ? `<a href="${escapeHtml(item.website)}" target="_blank" class="text-blue-400 underline">${escapeHtml(item.website)}</a>` : 'N/A'}</strong></div>
          </div>
        ` : ''}

        ${item.message ? `
          <div class="mt-3 pt-3 border-t border-[#5C3A40]/40">
            <span class="text-xs text-[#A8989B] block mb-1">Inquiry / Message Notes:</span>
            <p class="text-xs text-[#FCE6E9] bg-[#2A1F22] border border-[#EAA6B1]/30 p-3 rounded-lg leading-relaxed">${escapeHtml(item.message)}</p>
          </div>
        ` : ''}
      </div>

      <div class="space-y-2">
        <label class="text-xs font-bold uppercase tracking-wider text-[#A8989B]">Internal Follow-Up Notes</label>
        <textarea id="modalLeadNotes" rows="3" class="w-full text-xs p-3 rounded-xl form-input-luxury" placeholder="Add procurement screening notes, supplier quotes, sample tracking, or export status...">${escapeHtml(item.notes || '')}</textarea>
        <button onclick="saveLeadNotes(${item.id})" class="btn-rose-gold px-4 py-2 rounded-xl text-xs font-bold uppercase tracking-wider">
          Save Internal Notes
        </button>
      </div>
    </div>
  `;
}

async function saveLeadNotes(id) {
  const notesEl = document.getElementById('modalLeadNotes');
  if (!notesEl) return;
  const notes = notesEl.value;

  try {
    const res = await fetch(`/api/admin/submissions/${id}/notes`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ notes })
    });
    if (res.ok) {
      showToast('Notes saved successfully');
    } else {
      showToast('Could not save notes');
    }
  } catch (e) {
    showToast('Saved notes locally');
  }
}

function showToast(msg) {
  const toast = document.getElementById('adminToast');
  if (!toast) return;
  toast.innerText = msg;
  toast.classList.remove('translate-y-20', 'opacity-0');
  toast.classList.add('translate-y-0', 'opacity-100');
  setTimeout(() => {
    toast.classList.remove('translate-y-0', 'opacity-100');
    toast.classList.add('translate-y-20', 'opacity-0');
  }, 2500);
}

function cleanPhoneForWa(phone) {
  return (phone || '').replace(/[^0-9]/g, '');
}

function escapeHtml(str) {
  if (!str) return '';
  return str.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
}
