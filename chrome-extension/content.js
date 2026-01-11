// Keywords groups for checking
const designKeywords = ['design', 'method', 'making', 'applied art', 'intention', 'plan', 'research', 'tool', 'inquiry', 'practice', 'work', 'concept', 'craft', 'exploration', 'engineering', 'shape', 'project'];
const criticalKeywords = ['critical', 'conceptual', 'analytical', 'deconstructive', 'collaborative', 'interdisciplinary', 'contextual', 'iterative', 'reflective', 'theoretical', 'evaluative', 'investigative', 'explore', 'dialectical', 'discursive', 'reflexive', 'narrative', 'speculative', 'systemic'];

// Function to check if keywords are on the webpage
function checkKeywordsOnPage() {
  const pageText = document.body.innerText.toLowerCase();
  
  // Check for design keywords
  let designFound = [];
  let designNotFound = [];
  designKeywords.forEach(keyword => {
    const regex = new RegExp(`\\b${keyword.toLowerCase().replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\b`, 'g');
    if (regex.test(pageText)) {
      designFound.push(keyword);
    } else {
      designNotFound.push(keyword);
    }
  });
  
  // Check for critical keywords
  let criticalFound = [];
  let criticalNotFound = [];
  criticalKeywords.forEach(keyword => {
    const regex = new RegExp(`\\b${keyword.toLowerCase().replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\b`, 'g');
    if (regex.test(pageText)) {
      criticalFound.push(keyword);
    } else {
      criticalNotFound.push(keyword);
    }
  });
  
  console.log('=== Keyword Check ===');
  console.log('Design Keywords:');
  if (designFound.length > 0) {
    console.log('  ✓ Found:', designFound);
  }
  if (designNotFound.length > 0) {
    console.log('  ✗ Not found:', designNotFound);
  }
  
  console.log('Critical Keywords:');
  if (criticalFound.length > 0) {
    console.log('  ✓ Found:', criticalFound);
  }
  if (criticalNotFound.length > 0) {
    console.log('  ✗ Not found:', criticalNotFound);
  }
  
  const bothFound = designFound.length > 0 && criticalFound.length > 0;
  console.log(`\n${bothFound ? '✓' : '✗'} Both groups present:`, bothFound);
  
  return {
    hasBothGroups: bothFound,
    designKeywordsFound: designFound,
    criticalKeywordsFound: criticalFound
  };
}


// Keywords that trigger the connection line and navigation
const axisKeywords = new Set([
  'critical',
  'speculative',
  'conceptual',
  'reflective',
  'reflexive',
  'collaborative',
  'interdisciplinary',
  'iterative',
  'deconstructive',
  'analytical',
  'contextual',
  'narrative',
  'discursive',
  'dialectical',
  'systemic',
  'design'
]);

// Storage for keywords and their colors
let keywords = [];
let keywordColors = {};

// Storage for clicked elements and keywords
let clickedElements = [];
let clickedKeywords = new Set();

// Color palette - 35 distinct colors
const colors = [
  '#FFD700', // gold
  '#FF6B6B', // red
  '#4ECDC4', // teal
  '#95E1D3', // mint
  '#F38181', // pink
  '#AA96DA', // purple
  '#FCBAD3', // light pink
  '#A8D8EA', // light blue
  '#FFB4A2', // salmon
  '#E0BBE4', // lavender
  '#CAFFBF', // light green
  '#FFD6A5', // peach
  '#FFC6FF', // light purple
  '#BDB2FF', // periwinkle
  '#A0D995', // pistachio
  '#FF7F50', // coral
  '#6495ED', // cornflower blue
  '#DDA0DD', // plum
  '#F0E68C', // khaki
  '#FF69B4', // hot pink
  '#87CEEB', // sky blue
  '#98FB98', // pale green
  '#FFB347', // pastel orange
  '#DDA0DD', // orchid
  '#B0E0E6', // powder blue
  '#FFE4B5', // moccasin
  '#F0FFFF', // azure
  '#FFDAB9', // peach puff
  '#EEE8AA', // pale goldenrod
  '#F5DEB3', // wheat
  '#CD5C5C', // indian red
  '#66CDAA', // medium aquamarine
  '#7FFFD4', // aquamarine
  '#20B2AA', // light sea green
  '#FF8C00'  // dark orange
];

function updateKeywordStyles() {
  const marks = document.querySelectorAll('.keyword-highlight');
  marks.forEach(mark => {
    const keyword = mark.getAttribute('data-keyword');
    const isClicked = clickedElements.includes(mark);
    
    if (isClicked) {
      const color = keywordColors[keyword];
      // Add pink blur/glow effect
      mark.classList.add('clicked');
      mark.style.boxShadow = `0 0 15px #FF6600, 0 0 25px #FF6600`;
    } else {
      mark.classList.remove('clicked');
      mark.style.boxShadow = 'none';
    }
  });
}

let navigationTimer = null;

function handleKeywordClick(keyword, element) {
  console.log('Keyword clicked:', keyword);
  console.log('Current clicked elements before:', clickedElements.length, 'keywords before:', clickedKeywords.size);
  
  // Toggle element in clicked array
  const idx = clickedElements.indexOf(element);
  
  if (idx > -1) {
    // Already clicked this exact element, remove it
    clickedElements.splice(idx, 1);
    clickedKeywords.delete(keyword);
    console.log('Removed keyword:', keyword);
  } else {
    // Check if this keyword is already clicked (different element of same keyword)
    const existingIdx = clickedElements.findIndex(el => el.getAttribute('data-keyword') === keyword);
    if (existingIdx > -1) {
      // Replace the old instance with the new one
      clickedElements[existingIdx] = element;
      console.log('Replaced keyword element:', keyword);
    } else {
      // New keyword, add it
      clickedElements.push(element);
      clickedKeywords.add(keyword);
      console.log('Added keyword:', keyword);
    }
  }
  
  console.log('After click - elements:', clickedElements.length, 'keywords:', Array.from(clickedKeywords));
  
  // Update styles
  updateKeywordStyles();
  
  // Draw connection lines if 2 or more elements are selected
  if (clickedElements.length >= 2) {
    drawConnectionLine();
  } else {
    removeConnectionLine();
  }
  
  // Clear existing timer
  if (navigationTimer) {
    clearTimeout(navigationTimer);
  }
  
  // If we have selected keywords, set a timer to navigate
  if (clickedKeywords.size > 0) {
    console.log('Currently selected:', Array.from(clickedKeywords), 'Count:', clickedKeywords.size);
    console.log('⏱️  Will navigate in 2 seconds...');
    
    navigationTimer = setTimeout(() => {
      const keywords = Array.from(clickedKeywords);
      console.log('Navigating to 3D landscape with keywords:', keywords);
      
      // Build URL with keyword parameters
      const url = new URL('https://classy-genie-854a0e.netlify.app');
      keywords.forEach(kw => {
        url.searchParams.append('keyword', kw);
      });
      
      window.location.href = url.toString();
    }, 2000);
  }
}

function findBestSection(keyword1, keyword2) {
  console.log('🔍 Finding best section for:', keyword1, 'and', keyword2);
  // Get all paragraphs, divs, sections and articles
  const sections = document.querySelectorAll('p, div, section, article, h1, h2, h3, h4, h5, h6');
  console.log('Found', sections.length, 'potential sections to search');
  
  let bestSection = null;
  let highestScore = 0;
  
  sections.forEach(section => {
    const text = section.textContent.toLowerCase();
    const kw1Lower = keyword1.toLowerCase();
    const kw2Lower = keyword2.toLowerCase();
    
    // Count occurrences of both keywords in this section
    const kw1Count = (text.match(new RegExp(`\\b${kw1Lower}\\b`, 'g')) || []).length;
    const kw2Count = (text.match(new RegExp(`\\b${kw2Lower}\\b`, 'g')) || []).length;
    
    // Score is the product of both counts (high score when both keywords appear frequently)
    const score = kw1Count * kw2Count;
    
    if (score > highestScore && score > 0) {
      highestScore = score;
      bestSection = section;
    }
  });
  
  console.log('✅ Best section found with score:', highestScore);
  if (bestSection) {
    console.log('Section content:', bestSection.textContent.substring(0, 100));
  } else {
    console.log('❌ No section found with both keywords');
  }
  return bestSection;
}

function drawConnectionLine() {
  console.log('Drawing connection line...');
  
  if (clickedElements.length < 2) {
    console.log('Not enough elements clicked');
    return;
  }
  
  // Get positions of the specific clicked elements (page coordinates)
  const positions = [];
  clickedElements.forEach((element, idx) => {
    const rect = element.getBoundingClientRect();
    console.log(`Element ${idx}:`, rect);
    positions.push({
      x: rect.left + rect.width / 2 + window.scrollX,
      y: rect.top + rect.height / 2 + window.scrollY
    });
  });
  
  // Create or get SVG canvas
  let svg = document.getElementById('connection-svg');
  if (!svg) {
    console.log('Creating new SVG canvas');
    svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.id = 'connection-svg';
    svg.style.position = 'absolute';
    svg.style.top = '0';
    svg.style.left = '0';
    svg.style.pointerEvents = 'none';
    svg.style.zIndex = '999999';
    document.body.appendChild(svg);
  }
  
  // Set SVG to cover the entire document
  const docWidth = Math.max(document.body.scrollWidth, window.innerWidth);
  const docHeight = Math.max(document.body.scrollHeight, window.innerHeight);
  svg.setAttribute('width', docWidth);
  svg.setAttribute('height', docHeight);
  svg.setAttribute('viewBox', `0 0 ${docWidth} ${docHeight}`);
  
  // Clear previous lines
  while (svg.firstChild) {
    svg.removeChild(svg.firstChild);
  }
  
  // Draw lines connecting all keywords to each other
  for (let i = 0; i < positions.length; i++) {
    for (let j = i + 1; j < positions.length; j++) {
      console.log(`Drawing line from keyword ${i} to keyword ${j}`);
      const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
      line.setAttribute('x1', positions[i].x);
      line.setAttribute('y1', positions[i].y);
      line.setAttribute('x2', positions[j].x);
      line.setAttribute('y2', positions[j].y);
      line.setAttribute('stroke', '#FF6600');
      line.setAttribute('stroke-width', '4');
      line.setAttribute('stroke-linecap', 'round');
      svg.appendChild(line);
    }
  }
  
  // Add glowing circles at all endpoints
  positions.forEach((pos, i) => {
    const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    circle.setAttribute('cx', pos.x);
    circle.setAttribute('cy', pos.y);
    circle.setAttribute('r', '6');
    circle.setAttribute('fill', '#FF6600');
    circle.setAttribute('opacity', '0.8');
    circle.setAttribute('filter', 'drop-shadow(0 0 8px #FF6600)');
    svg.appendChild(circle);
  });
  
  console.log('Connection line drawn successfully');
}

function removeConnectionLine() {
  const svg = document.getElementById('connection-svg');
  if (svg) {
    svg.remove();
  }
}

async function loadKeywords() {
  console.log('🚀 Starting loadKeywords()...');
  try {
    // Load keywords from keywords.js
    console.log('📄 Fetching keywords.js...');
    const keywordsResponse = await fetch(chrome.runtime.getURL('keywords.js'));
    console.log('✅ Keywords.js response:', keywordsResponse.status);
    const keywordsText = await keywordsResponse.text();
    console.log('📝 Keywords text length:', keywordsText.length);
    
    // Parse keywords.js without eval (CSP-safe)
    const keywordsMatch = keywordsText.match(/const keywords\s*=\s*({[\s\S]+?});\s*export default/);
    console.log('🔍 Keywords match found:', !!keywordsMatch);
    if (keywordsMatch) {
      // Use JSON.parse instead of eval to avoid CSP issues
      const keywordsData = JSON.parse(keywordsMatch[1]);
      console.log('📦 Keywords data parsed:', Object.keys(keywordsData));
      
      // Extract all keywords from both design_group and critical_group
      for (const [groupName, group] of Object.entries(keywordsData)) {
        for (const [keyword, variations] of Object.entries(group)) {
          const lowerKeyword = keyword.toLowerCase();
          if (!keywords.includes(lowerKeyword)) {
            keywords.push(lowerKeyword);
          }
        }
      }
      console.log('✅ Extracted', keywords.length, 'keywords');
    }
    
    // Load consolidated keywords with colors
    console.log('Loading keywords_with_colors.json...');
    const keywordsWithColorsResponse = await fetch(chrome.runtime.getURL('keywords_with_colors.json'));
    if (!keywordsWithColorsResponse.ok) throw new Error(`Failed to load keywords_with_colors.json: ${keywordsWithColorsResponse.status}`);
    const keywordColorMap = await keywordsWithColorsResponse.json();
    console.log('Loaded ' + Object.keys(keywordColorMap).length + ' keywords');
    
    // Use keywords and colors directly from the JSON
    keywords = Object.keys(keywordColorMap);
    keywordColors = keywordColorMap;
    
    console.log('Starting highlighting with ' + keywords.length + ' keywords');
    highlightKeywords();
  } catch (error) {
    console.error('❌ Error loading keywords:', error);
    console.log('⚠️  Falling back to hardcoded keywords');
    // Fallback to hardcoded keywords
    const allKeywords = new Set([...designKeywords, ...criticalKeywords]);
    
    var colorIndex = 0;
    allKeywords.forEach(keyword => {
      const lowerKeyword = keyword.toLowerCase();
      if (!keywords.includes(lowerKeyword)) {
        keywords.push(lowerKeyword);
        keywordColors[lowerKeyword] = colors[colorIndex % colors.length];
        colorIndex++;
      }
    });
    console.log('⚠️  Using', keywords.length, 'hardcoded keywords');
    highlightKeywords();
  }
}

function highlightKeywords() {
  // Don't highlight on the landscape page
  const isLandscapePage = window.location.href.includes('classy-genie-854a0e.netlify.app') || 
                          window.location.href.includes('localhost');
  
  if (isLandscapePage) {
    console.log('Skipping keyword highlighting on landscape page');
    return;
  }
  
  if (keywords.length === 0) {
    console.log('No keywords loaded yet');
    return;
  }
  
  console.log('Starting keyword highlighting with ' + keywords.length + ' keywords');
  console.log('Keywords to highlight:', keywords.slice(0, 10));
  
  const walker = document.createTreeWalker(
    document.body,
    NodeFilter.SHOW_TEXT,
    null,
    false
  );
  
  const nodesToProcess = [];
  let node;
  
  while (node = walker.nextNode()) {
    nodesToProcess.push(node);
  }
  
  nodesToProcess.forEach(textNode => {
    // Skip text in certain elements that shouldn't be modified
    const parent = textNode.parentElement;
    const skipTags = ['BUTTON', 'INPUT', 'TEXTAREA', 'SELECT', 'SCRIPT', 'STYLE', 'NOSCRIPT', 'SVG', 'IMG', 'VIDEO', 'AUDIO', 'IFRAME', 'CODE', 'PRE'];
    const skipClasses = ['goog-', 'google-', 'icon', 'btn', 'logo', 'nav'];
    
    const parentClassName = String(parent?.className || '');
    if (skipTags.includes(parent?.tagName) || skipClasses.some(cls => parentClassName.includes(cls))) {
      return;
    }
    
    // Skip very short text (likely UI elements)
    const text = textNode.textContent;
    if (text.trim().length < 3) {
      return;
    }
    
    let hasKeyword = false;
    
    // Check if any keyword is in this text
    for (let keyword of keywords) {
      if (text.toLowerCase().includes(keyword)) {
        hasKeyword = true;
        break;
      }
    }
    
    if (!hasKeyword) return;
    
    // Create a minimal inline span to hold the highlighted content
    const span = document.createElement('span');
    let html = text;
    
    // Sort keywords by length (longest first) to avoid nested replacements
    const sortedKeywords = [...keywords].sort((a, b) => b.length - a.length);
    
    for (let keyword of sortedKeywords) {
      const regex = new RegExp(`\\b${keyword}\\b`, 'gi');
      const color = keywordColors[keyword] || '#CCCCCC';
      html = html.replace(regex, `<mark class="keyword-highlight" data-keyword="${keyword}" style="background-color: ${color}; cursor: pointer;">$&</mark>`);
    }
    
    span.innerHTML = html;
    
    // Add click handlers to all highlighted keywords
    const marks = span.querySelectorAll('.keyword-highlight');
    marks.forEach(mark => {
      mark.addEventListener('click', (e) => {
        e.stopPropagation();
        const keyword = mark.getAttribute('data-keyword');
        handleKeywordClick(keyword, mark); // Pass the element reference
      });
      
      mark.addEventListener('mouseenter', () => {
        mark.style.cursor = 'pointer';
      });
      mark.addEventListener('mouseleave', () => {
        mark.style.cursor = 'pointer';
      });
    });
    
    textNode.parentNode.replaceChild(span, textNode);
  });
  
  // Initial style update
  updateKeywordStyles();
  console.log('✅ Keyword highlighting complete');
}

// Load designer names FIRST, then keywords
async function loadDesigners() {
  try {
    console.log('Starting designer highlighting...');
    const response = await fetch(chrome.runtime.getURL('designers.json'));
    console.log('Response status:', response.ok, response.status);
    
    if (!response.ok) {
      console.log('Failed to load designers.json');
      return;
    }
    
    const designers = await response.json();
    console.log('Loaded designers:', designers.length);
    console.log('Designers:', designers.map(d => d.name).join(', '));
    
    if (designers.length === 0) {
      console.log('No designers found');
      return;
    }
    
    // Sort by name length (longest first)
    const sortedDesigners = designers.sort((a, b) => b.name.length - a.name.length);
    
    const walker = document.createTreeWalker(
      document.body,
      NodeFilter.SHOW_TEXT,
      null,
      false
    );
    
    const nodesToReplace = [];
    let textNode;
    while (textNode = walker.nextNode()) {
      nodesToReplace.push(textNode);
    }
    
    console.log('Text nodes to process:', nodesToReplace.length);
    
    let highlightCount = 0;
    nodesToReplace.forEach((node, nodeIndex) => {
      let text = node.textContent;
      let modified = false;
      
      sortedDesigners.forEach(designer => {
        const escapedName = designer.name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        const regex = new RegExp(`\\b${escapedName}\\b`, 'gi');
        
        if (regex.test(text)) {
          console.log(`Found "${designer.name}"`);
          modified = true;
          text = text.replace(regex, `[DESIGNER::${designer.name}::]`);
          highlightCount++;
        }
      });
      
      if (modified) {
        const span = document.createElement('span');
        let html = text;
        
        sortedDesigners.forEach(designer => {
          const placeholder = `[DESIGNER::${designer.name}::]`;
          html = html.split(placeholder).join(`<a href="${designer.url}" target="_blank" style="background-color: black; color: white; padding: 2px 4px; text-decoration: none; cursor: pointer; border-radius: 2px;">${designer.name}</a>`);
        });
        
        span.innerHTML = html;
        node.parentNode.replaceChild(span, node);
      }
    });
    
    console.log('Designer highlighting complete. Highlighted:', highlightCount);
    
  } catch (error) {
    console.error('Designer highlighting error:', error);
  }
}

// Load keywords when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', async () => {
    await loadDesigners();
    loadKeywords();
  });
} else {
  loadDesigners().then(() => loadKeywords());
}

// Load designer names after a short delay
setTimeout(async () => {
  try {
    console.log('Starting designer highlighting...');
    const response = await fetch(chrome.runtime.getURL('designers.json'));
    console.log('Response status:', response.ok, response.status);
    
    if (!response.ok) {
      console.log('Failed to load designers.json');
      return;
    }
    
    const designers = await response.json();
    console.log('Loaded designers:', designers.length);
    console.log('Designers:', designers.map(d => d.name).join(', '));
    
    if (designers.length === 0) {
      console.log('No designers found');
      return;
    }
    
    // Sort by name length (longest first) to handle longer names before shorter ones
    const sortedDesigners = designers.sort((a, b) => b.name.length - a.name.length);
    
    // Find and highlight designer names in all text nodes
    const walker = document.createTreeWalker(
      document.body,
      NodeFilter.SHOW_TEXT,
      null,
      false
    );
    
    const nodesToReplace = [];
    let textNode;
    while (textNode = walker.nextNode()) {
      nodesToReplace.push(textNode);
    }
    
    console.log('Text nodes to process:', nodesToReplace.length);
    
    let highlightCount = 0;
    nodesToReplace.forEach((node, nodeIndex) => {
      let text = node.textContent;
      let modified = false;
      
      sortedDesigners.forEach(designer => {
        // Escape special regex characters
        const escapedName = designer.name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        const regex = new RegExp(`\\b${escapedName}\\b`, 'gi');
        
        if (regex.test(text)) {
          console.log(`Found "${designer.name}"`);
          modified = true;
          text = text.replace(regex, `[DESIGNER::${designer.name}::]`);
          highlightCount++;
        }
      });
      
      if (modified) {
        const span = document.createElement('span');
        let html = text;
        
        sortedDesigners.forEach(designer => {
          const placeholder = `[DESIGNER::${designer.name}::]`;
          html = html.split(placeholder).join(`<a href="${designer.url}" target="_blank" style="background-color: black; color: white; padding: 2px 4px; text-decoration: none; cursor: pointer; border-radius: 2px;">${designer.name}</a>`);
        });
        
        span.innerHTML = html;
        node.parentNode.replaceChild(span, node);
      }
    });
    
    console.log('Designer highlighting complete. Highlighted:', highlightCount);
    
  } catch (error) {
    console.error('Designer highlighting error:', error);
  }
}, 1000);

// Add ADD button to the page
function addCritLogo() {
  // Create style for the button
  const style = document.createElement('style');
  style.textContent = `
    @import url('https://fonts.googleapis.com/css2?family=Arimo:wght@400&display=swap');
    
    body::before {
      content: '';
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      box-shadow: inset 0 0 40px #FF6600;
      pointer-events: none;
      z-index: 2147483646;
    }
    
    #crit-add-button {
      position: fixed;
      bottom: 25px;
      right: 25px;
      width: 40px;
      height: 40px;
      border-radius: 50%;
      background-color: transparent;
      color: #666;
      border: 1.5px solid #666;
      cursor: pointer;
      font-size: 11px;
      font-weight: bold;
      font-family: "Arimo", Arial, sans-serif;
      z-index: 2147483647;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.2s ease;
      padding: 0;
    }

    #crit-add-button:hover {
      border-color: #666;
      color: #666;
      transform: scale(1.05);
    }
  `;
  document.head.appendChild(style);

  // Create the ADD button
  const addButton = document.createElement('button');
  addButton.id = 'crit-add-button';
  addButton.textContent = 'ADD';
  addButton.addEventListener('click', async () => {
    const currentURL = window.location.href;
    console.log('🔵 ADD button clicked on:', currentURL);
    
    // Check keywords on page
    const keywordCheck = checkKeywordsOnPage();
    
    // Validate: must have at least one keyword from each group
    if (!keywordCheck.hasBothGroups) {
      console.log('❌ Page missing keywords from both groups!');
      console.log('   - Design group found:', keywordCheck.designKeywordsFound.length > 0 ? '✓' : '✗');
      console.log('   - Critical group found:', keywordCheck.criticalKeywordsFound.length > 0 ? '✓' : '✗');
      return;
    }
    
    // Check if URL is already in nodes.json
    try {
      const nodesUrl = chrome.runtime.getURL('nodes.json');
      const nodesResponse = await fetch(nodesUrl);
      const nodes = await nodesResponse.json();
      
      const isAlreadyInList = nodes.some(node => node.url === currentURL);
      
      if (isAlreadyInList) {
        console.log('⚠️  URL already exists in the landscape!');
        return;
      }
      
      // All checks passed - add to list
      console.log('✅ All checks passed!');
      console.log('   - Design keywords:', keywordCheck.designKeywordsFound.join(', '));
      console.log('   - Critical keywords:', keywordCheck.criticalKeywordsFound.join(', '));
      console.log('   - Not in list: proceeding to add');
      
      // Insert directly to MongoDB via Netlify function
      const SERVER_URL = 'https://classy-genie-854a0e.netlify.app/.netlify/functions/add-url';
      
      fetch(SERVER_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          url: currentURL,
          designKeywords: keywordCheck.designKeywordsFound,
          criticalKeywords: keywordCheck.criticalKeywordsFound
        })
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          console.log('✓ URL saved! Total URLs:', data.totalUrls);
          alert('✓ URL added to landscape database!');
        } else {
          console.error('❌ Failed:', data.error);
          alert('❌ Error: ' + data.error);
        }
      })
      .catch(error => {
        console.error('❌ Error:', error);
      });
    } catch (error) {
      console.error('❌ Error checking nodes.json:', error);
    }
  });
  document.body.appendChild(addButton);
}

// Add the logo when the page loads (but not on the landscape page)
const isLandscapePage = window.location.href.includes('classy-genie-854a0e.netlify.app') || 
                        window.location.href.includes('127.0.0.1:5500/landscape');
if (!isLandscapePage) {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', addCritLogo);
  } else {
    addCritLogo();
  }
}
