document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('analyzeForm');
  const fileInput = document.getElementById('docFile');
  const fileNameDisplay = document.getElementById('fileName');
  const submitBtn = document.getElementById('submitBtn');
  const loader = document.getElementById('loader');
  const errorBanner = document.getElementById('errorBanner');
  const resultsSection = document.getElementById('resultsSection');
  
  const scoreVal = document.getElementById('scoreVal');
  const verdictBadge = document.getElementById('verdictBadge');
  const verdictDescription = document.getElementById('verdictDescription');
  const evidenceList = document.getElementById('evidenceList');

  // Update file name display when file is selected
  fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) {
      fileNameDisplay.textContent = fileInput.files[0].name;
    } else {
      fileNameDisplay.textContent = 'Drag and drop file here or click to browse';
    }
  });

  // Descriptions for each verdict type
  const descriptions = {
    'Highly Recommended': 'This document provides deep and repeated coverage of your query topic. It is well-suited for comprehensive study.',
    'Good for Reference': 'This document contains dedicated sections on this topic, suitable for reference or review.',
    'Passing Mention': 'The topic is only mentioned briefly or tangentially. It may not provide enough depth on its own.',
    'Not Suitable': 'No meaningful discussion of this topic was found in this document.'
  };

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Reset UI state
    errorBanner.classList.add('hidden');
    resultsSection.classList.add('hidden');
    loader.classList.remove('hidden');
    submitBtn.disabled = true;

    const formData = new FormData(form);

    try {
      const response = await fetch('/api/analyze', {
        method: 'POST',
        body: formData
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to analyze document.');
      }

      // Populate results
      scoreVal.textContent = `${data.score_percentage}%`;
      verdictBadge.textContent = data.verdict;
      
      // Assign appropriate color class to badge
      verdictBadge.className = 'verdict-badge';
      const badgeClass = `badge-${data.verdict.toLowerCase().replace(/\s+/g, '-')}`;
      verdictBadge.classList.add(badgeClass);

      verdictDescription.textContent = descriptions[data.verdict] || '';

      // Populate evidence snippets
      evidenceList.innerHTML = '';
      data.evidence.forEach((item, index) => {
        const card = document.createElement('div');
        card.className = 'evidence-card';
        card.innerHTML = `
          <div class="evidence-header">
            <span>Snippet #${index + 1}</span>
            <span>Match: ${item.score}%</span>
          </div>
          <p class="evidence-text">"...${escapeHtml(item.text)}..."</p>
        `;
        evidenceList.appendChild(card);
      });

      resultsSection.classList.remove('hidden');
    } catch (err) {
      errorBanner.textContent = err.message;
      errorBanner.classList.remove('hidden');
    } finally {
      loader.classList.add('hidden');
      submitBtn.disabled = false;
    }
  });

  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
});