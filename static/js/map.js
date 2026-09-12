/**
 * Tradenza International - Interactive Global Trade Map Visualizer
 * Rethemed for Obsidian & Rose Gold brand aesthetic.
 * Visualizes India as the Premier Sourcing Hub connecting to target global markets.
 */

document.addEventListener('DOMContentLoaded', () => {
  const mapContainer = document.getElementById('tradeMapContainer');
  if (!mapContainer) return;

  const INDIA_HUB = {
    id: 'india',
    name: 'India (Sourcing Hub)',
    city: 'Mumbai / Delhi / Mundra',
    x: 635,
    y: 235,
    type: 'hub',
    desc: 'National Sourcing & Export Epicenter: Agricultural, Spices, Textiles, Engineering, Ceramics & Building Materials'
  };

  const TARGET_MARKETS = [
    {
      id: 'uae',
      region: 'middle-east',
      name: 'United Arab Emirates',
      corridor: 'Arabian Gulf / Jebel Ali Hub',
      x: 550,
      y: 220,
      leadTime: 'Fast Sea Freight: 3–5 Days',
      products: 'Basmati Rice, Spices, Fresh Produce, Building Materials, Consumer Goods'
    },
    {
      id: 'saudi',
      region: 'middle-east',
      name: 'Saudi Arabia',
      corridor: 'Red Sea & Western Asia Corridor',
      x: 520,
      y: 235,
      leadTime: 'Direct Sea Transit: 4–7 Days',
      products: 'Grains, Foodstuffs, Textiles, Ceramic Tiles, Sanitaryware'
    },
    {
      id: 'usa',
      region: 'americas',
      name: 'United States of America',
      corridor: 'Transatlantic & Transpacific Gateway',
      x: 210,
      y: 180,
      leadTime: 'Ocean Freight: 22–28 Days / Air Express',
      products: 'Apparel, Spices, Organic Food, Medical Supplies, Home Furnishings'
    },
    {
      id: 'uk',
      region: 'europe',
      name: 'United Kingdom',
      corridor: 'British Isles Maritime Corridor',
      x: 460,
      y: 140,
      leadTime: 'Direct Port Routes: 18–22 Days',
      products: 'Textiles, Floor Tiles, Basmati, Spices, Consumer & Packaging Products'
    },
    {
      id: 'europe',
      region: 'europe',
      name: 'Continental Europe (EU)',
      corridor: 'Rotterdam / Antwerp / Hamburg Gateway',
      x: 490,
      y: 155,
      leadTime: 'Continental Maritime: 20–24 Days',
      products: 'Certified Agro Goods, Technical Textiles, Tiles, Medical Consumables'
    },
    {
      id: 'africa',
      region: 'africa',
      name: 'Africa (East & Southern Africa)',
      corridor: 'Indian Ocean Commercial Route',
      x: 535,
      y: 320,
      leadTime: 'Direct Shipping: 8–14 Days',
      products: 'Grains, Industrial Packaging, Tiles, Consumer Products, Fabrics'
    },
    {
      id: 'seasia',
      region: 'asia',
      name: 'Southeast Asia (ASEAN)',
      corridor: 'Straits of Malacca / Singapore Hub',
      x: 750,
      y: 275,
      leadTime: 'Direct Sea Freight: 5–8 Days',
      products: 'Spices, Agricultural Commodities, Fruits, Engineering Components'
    },
    {
      id: 'nepal',
      region: 'asia',
      name: 'Nepal',
      corridor: 'Regional Overland Cross-Border Corridor',
      x: 670,
      y: 205,
      leadTime: 'Direct Overland Transit: 1–3 Days',
      products: 'Food & Grains, Construction Materials, Consumer Goods, Packaging'
    }
  ];

  function renderMap(activeFilter = 'all') {
    function generateCurvedPath(x1, y1, x2, y2) {
      const mx = (x1 + x2) / 2;
      const my = (y1 + y2) / 2;
      const dx = x2 - x1;
      const dy = y2 - y1;
      const dist = Math.sqrt(dx * dx + dy * dy);
      
      const curvature = dist * 0.22;
      const cx = mx;
      const cy = my - curvature;
      return `M ${x1} ${y1} Q ${cx} ${cy} ${x2} ${y2}`;
    }

    const filteredMarkets = activeFilter === 'all' 
      ? TARGET_MARKETS 
      : TARGET_MARKETS.filter(m => m.region === activeFilter);

    let arcsSvg = '';
    let nodesSvg = '';

    filteredMarkets.forEach((market, idx) => {
      const pathD = generateCurvedPath(INDIA_HUB.x, INDIA_HUB.y, market.x, market.y);
      const delay = (idx * 0.35).toFixed(1);
      
      arcsSvg += `
        <g class="trade-route-group" data-target="${market.id}">
          <path d="${pathD}" fill="none" stroke="rgba(212, 148, 158, 0.18)" stroke-width="3" class="route-bg" />
          <path d="${pathD}" fill="none" stroke="url(#roseGoldMapGrad)" stroke-width="1.8" class="animated-trade-arc" style="animation-delay: ${delay}s;" />
        </g>
      `;

      nodesSvg += `
        <g class="market-node cursor-pointer transition-transform duration-300 hover:scale-125" 
           data-id="${market.id}" 
           data-name="${market.name}" 
           data-corridor="${market.corridor}" 
           data-transit="${market.leadTime}" 
           data-products="${market.products}"
           transform="translate(${market.x}, ${market.y})">
          <circle r="12" fill="rgba(212, 148, 158, 0.12)" />
          <circle r="6" fill="#191214" stroke="#EAA6B1" stroke-width="2" />
          <circle r="2.5" fill="#FCE6E9" />
          <text y="${market.y > 250 ? 18 : -12}" x="0" text-anchor="middle" 
                font-family="'Plus Jakarta Sans', sans-serif" 
                font-size="9.5" font-weight="700" fill="#FCE6E9" 
                class="pointer-events-none drop-shadow-md">
            ${market.name}
          </text>
        </g>
      `;
    });

    const svgHtml = `
      <svg viewBox="0 0 1000 480" class="w-full h-auto select-none" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id="roseGoldMapGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#FCE6E9" />
            <stop offset="50%" stop-color="#EAA6B1" />
            <stop offset="100%" stop-color="#C77F8B" />
          </linearGradient>
          <radialGradient id="hubGlowRose" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stop-color="#EAA6B1" stop-opacity="0.8" />
            <stop offset="40%" stop-color="#EAA6B1" stop-opacity="0.3" />
            <stop offset="100%" stop-color="#EAA6B1" stop-opacity="0" />
          </radialGradient>
          <pattern id="gridPatternDark" width="40" height="40" patternUnits="userSpaceOnUse">
            <path d="M 40 0 L 0 0 0 40" fill="none" stroke="rgba(212, 148, 158, 0.04)" stroke-width="1"/>
          </pattern>
        </defs>

        <rect width="1000" height="480" fill="#120D0E" rx="16"/>
        <rect width="1000" height="480" fill="url(#gridPatternDark)" rx="16"/>

        <g fill="rgba(40, 29, 32, 0.45)" stroke="rgba(212, 148, 158, 0.08)" stroke-width="1">
          <!-- Continents -->
          <path d="M 120,80 L 260,70 L 310,130 L 280,210 L 210,230 L 190,280 L 160,250 L 130,170 Z" />
          <path d="M 270,270 L 340,290 L 360,380 L 320,460 L 280,410 L 260,330 Z" />
          <path d="M 440,80 L 530,70 L 550,140 L 480,180 L 440,140 Z" />
          <path d="M 460,190 L 570,180 L 600,280 L 560,420 L 490,380 L 450,260 Z" />
          <path d="M 550,70 L 820,80 L 880,180 L 800,280 L 720,290 L 670,200 L 570,150 Z" />
          <!-- India Subcontinent Highlight -->
          <path d="M 615,200 L 665,190 L 670,240 L 640,285 L 618,245 Z" fill="rgba(212, 148, 158, 0.16)" stroke="#EAA6B1" stroke-width="1.2" />
          <path d="M 780,340 L 880,330 L 890,410 L 810,430 L 770,380 Z" />
        </g>

        <!-- Trade Arcs -->
        <g id="tradeRoutesLayer">
          ${arcsSvg}
        </g>

        <!-- Destination Nodes -->
        <g id="marketNodesLayer">
          ${nodesSvg}
        </g>

        <!-- Central India Sourcing Hub -->
        <g id="indiaHubGroup" transform="translate(${INDIA_HUB.x}, ${INDIA_HUB.y})" class="cursor-pointer">
          <circle r="36" fill="url(#hubGlowRose)" class="hub-pulse" />
          <circle r="22" fill="none" stroke="#EAA6B1" stroke-width="1.5" opacity="0.6" class="hub-pulse" style="animation-delay: 1.2s;" />
          
          <!-- Outer Hexagon Icon for Hub -->
          <polygon points="0,-12 10,-6 10,6 0,12 -10,6 -10,-6" fill="#191214" stroke="#EAA6B1" stroke-width="2" />
          <circle r="3" fill="#FCE6E9" />
          
          <rect x="-65" y="-38" width="130" height="24" rx="12" fill="#191214" stroke="#EAA6B1" stroke-width="1.5" />
          <text x="0" y="-23" text-anchor="middle" font-family="'Plus Jakarta Sans', sans-serif" font-size="10.5" font-weight="800" fill="#FCE6E9" letter-spacing="0.5">
            ★ INDIA (HUB)
          </text>
        </g>
      </svg>
    `;

    mapContainer.innerHTML = svgHtml;
    attachMapInteractions();
  }

  function attachMapInteractions() {
    const tooltip = document.getElementById('mapTooltip');
    const nodes = mapContainer.querySelectorAll('.market-node');
    const hubNode = mapContainer.querySelector('#indiaHubGroup');

    nodes.forEach(node => {
      node.addEventListener('mouseenter', () => {
        const name = node.dataset.name;
        const corridor = node.dataset.corridor;
        const transit = node.dataset.transit;
        const products = node.dataset.products;

        if (tooltip) {
          tooltip.innerHTML = `
            <div class="p-3.5 bg-[#191214]/95 border border-[#EAA6B1]/40 rounded-xl shadow-2xl backdrop-blur-md max-w-xs text-left">
              <div class="flex items-center gap-2 mb-1.5">
                <span class="w-2.5 h-2.5 rounded-full bg-[#EAA6B1] animate-ping"></span>
                <h4 class="font-bold text-white text-sm tracking-wide">${name}</h4>
              </div>
              <p class="text-xs text-[#FCE6E9] font-semibold mb-1">${corridor}</p>
              <p class="text-[11px] text-[#EDE4E5] mb-2">Transit: <span class="text-white font-medium">${transit}</span></p>
              <div class="border-t border-[#5C3A40]/70 pt-1.5">
                <span class="text-[10px] uppercase font-bold text-[#A8989B] tracking-wider">Key Sourced Goods:</span>
                <p class="text-[11px] text-[#EFE6E7] mt-0.5 leading-relaxed">${products}</p>
              </div>
            </div>
          `;
          tooltip.classList.remove('hidden');
        }
      });

      node.addEventListener('mousemove', (e) => {
        if (tooltip) {
          const rect = mapContainer.getBoundingClientRect();
          const x = e.clientX - rect.left + 15;
          const y = e.clientY - rect.top + 15;
          tooltip.style.left = `${x}px`;
          tooltip.style.top = `${y}px`;
        }
      });

      node.addEventListener('mouseleave', () => {
        if (tooltip) tooltip.classList.add('hidden');
      });
    });

    if (hubNode) {
      hubNode.addEventListener('mouseenter', () => {
        if (tooltip) {
          tooltip.innerHTML = `
            <div class="p-3.5 bg-[#191214]/95 border border-[#EAA6B1]/50 rounded-xl shadow-2xl backdrop-blur-md max-w-xs text-left">
              <div class="flex items-center gap-2 mb-1">
                <span class="text-[#FCE6E9]">★</span>
                <h4 class="font-bold text-white text-sm">India — Sourcing & Export Hub</h4>
              </div>
              <p class="text-xs text-[#EDE4E5] leading-relaxed mt-1">
                ${INDIA_HUB.desc}
              </p>
              <p class="text-[11px] text-[#FCE6E9] font-medium mt-2">Ports: Mundra, Nhava Sheva, Chennai, Vizag, Cochin</p>
            </div>
          `;
          tooltip.classList.remove('hidden');
        }
      });

      hubNode.addEventListener('mousemove', (e) => {
        if (tooltip) {
          const rect = mapContainer.getBoundingClientRect();
          const x = e.clientX - rect.left + 15;
          const y = e.clientY - rect.top + 15;
          tooltip.style.left = `${x}px`;
          tooltip.style.top = `${y}px`;
        }
      });

      hubNode.addEventListener('mouseleave', () => {
        if (tooltip) tooltip.classList.add('hidden');
      });
    }
  }

  const filterButtons = document.querySelectorAll('.map-filter-btn');
  filterButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      filterButtons.forEach(b => {
        b.classList.remove('bg-[#EAA6B1]', 'text-[#120D0E]');
        b.classList.add('bg-[#22181B]', 'text-[#EDE4E5]');
      });
      btn.classList.remove('bg-[#22181B]', 'text-[#EDE4E5]');
      btn.classList.add('bg-[#EAA6B1]', 'text-[#120D0E]');

      const filter = btn.dataset.filter || 'all';
      renderMap(filter);
    });
  });

  renderMap('all');
});
