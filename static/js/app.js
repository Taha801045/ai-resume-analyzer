/**
 * ResuMetric AI - Main Frontend Application Logic
 */

// Application State
const state = {
  theme: localStorage.getItem('theme') || 'dark',
  currentTab: 'overview',
  analysisData: null,
  selectedFile: null,
  apiKey: localStorage.getItem('gemini_api_key') || '',
  apiProvider: localStorage.getItem('api_provider') || 'local',
  chartInstance: null,
};

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initEventListeners();
  initDropzone();
  checkHealth();
});

// Theme Management
function initTheme() {
  if (state.theme === 'dark') {
    document.documentElement.classList.add('dark');
  } else {
    document.documentElement.classList.remove('dark');
  }
  updateThemeIcon();
}

function toggleTheme() {
  state.theme = state.theme === 'dark' ? 'light' : 'dark';
  localStorage.setItem('theme', state.theme);
  initTheme();
  if (state.chartInstance && state.analysisData) {
    renderRadarChart(state.analysisData.breakdown);
  }
}

function updateThemeIcon() {
  const icon = document.getElementById('theme-toggle-icon');
  if (!icon) return;
  if (state.theme === 'dark') {
    icon.innerHTML = `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />`;
  } else {
    icon.innerHTML = `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />`;
  }
}

// Health Check
async function checkHealth() {
  try {
    const res = await fetch('/health');
    if (res.ok) {
      const badge = document.getElementById('system-status');
      if (badge) {
        badge.innerHTML = `<span class="w-2 h-2 rounded-full bg-emerald-500 pulse-indicator mr-2"></span> AI Engine: Ready`;
      }
    }
  } catch (err) {
    const badge = document.getElementById('system-status');
    if (badge) {
      badge.innerHTML = `<span class="w-2 h-2 rounded-full bg-amber-500 pulse-indicator mr-2"></span> Client-Ready Mode`;
    }
  }
}

// Event Listeners
function initEventListeners() {
  document.getElementById('theme-toggle')?.addEventListener('click', toggleTheme);

  // Tab switching
  document.querySelectorAll('.tab-btn').forEach((btn) => {
    btn.addEventListener('click', (e) => {
      const tabId = btn.getAttribute('data-tab');
      switchTab(tabId);
    });
  });

  // Sample load buttons
  document.querySelectorAll('.sample-btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      const role = btn.getAttribute('data-role');
      loadSample(role);
    });
  });

  // Form submit
  document.getElementById('analyze-form')?.addEventListener('submit', (e) => {
    e.preventDefault();
    runAnalysis();
  });

  // Settings modal
  document.getElementById('open-settings')?.addEventListener('click', openSettings);
  document.getElementById('close-settings')?.addEventListener('click', closeSettings);
  document.getElementById('save-settings')?.addEventListener('click', saveSettings);

  // Print report
  document.getElementById('btn-print-report')?.addEventListener('click', () => {
    window.print();
  });

  // Bullet optimizer submit
  document.getElementById('btn-run-optimizer')?.addEventListener('click', runBulletOptimizer);

  // Reset button
  document.getElementById('btn-reset')?.addEventListener('click', resetAll);
}

// Drag & Drop File Upload
function initDropzone() {
  const dropzone = document.getElementById('dropzone');
  const fileInput = document.getElementById('file-input');
  if (!dropzone || !fileInput) return;

  ['dragenter', 'dragover'].forEach((eventName) => {
    dropzone.addEventListener(eventName, (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropzone.classList.add('dropzone-active');
    });
  });

  ['dragleave', 'drop'].forEach((eventName) => {
    dropzone.addEventListener(eventName, (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropzone.classList.remove('dropzone-active');
    });
  });

  dropzone.addEventListener('drop', (e) => {
    const dt = e.dataTransfer;
    const files = dt.files;
    if (files.length > 0) {
      handleFileSelected(files[0]);
    }
  });

  fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
      handleFileSelected(e.target.files[0]);
    }
  });
}

function handleFileSelected(file) {
  state.selectedFile = file;
  const fileNameDisplay = document.getElementById('file-selected-name');
  const fileInfoBox = document.getElementById('file-info-box');
  const dropPrompt = document.getElementById('drop-prompt');

  if (fileNameDisplay) {
    const sizeKb = (file.size / 1024).toFixed(1);
    fileNameDisplay.textContent = `${file.name} (${sizeKb} KB)`;
  }
  if (fileInfoBox && dropPrompt) {
    fileInfoBox.classList.remove('hidden');
    dropPrompt.classList.add('hidden');
  }

  // Clear text area to indicate file mode
  const resumeTextEl = document.getElementById('resume-text');
  if (resumeTextEl) {
    resumeTextEl.value = `[Selected File: ${file.name}]`;
  }
}

function clearSelectedFile(e) {
  if (e) e.stopPropagation();
  state.selectedFile = null;
  const fileInput = document.getElementById('file-input');
  if (fileInput) fileInput.value = '';
  const fileInfoBox = document.getElementById('file-info-box');
  const dropPrompt = document.getElementById('drop-prompt');
  const resumeTextEl = document.getElementById('resume-text');

  if (fileInfoBox) fileInfoBox.classList.add('hidden');
  if (dropPrompt) dropPrompt.classList.remove('hidden');
  if (resumeTextEl) resumeTextEl.value = '';
}
window.clearSelectedFile = clearSelectedFile;

// Load Sample Profiles
async function loadSample(role) {
  showLoading('Loading industry-standard candidate profile...');
  try {
    const res = await fetch(`/api/sample?role=${role}`);
    const data = await res.json();
    if (data.success) {
      clearSelectedFile();
      const resumeTextEl = document.getElementById('resume-text');
      const jdTextEl = document.getElementById('job-description');

      if (resumeTextEl) resumeTextEl.value = data.resume;
      if (jdTextEl) jdTextEl.value = data.job_description;

      // Automatically run analysis to demonstrate speed
      await runAnalysis();
    }
  } catch (err) {
    console.error('Failed to load sample:', err);
    hideLoading();
  }
}

// Run Full Analysis
async function runAnalysis() {
  const resumeText = document.getElementById('resume-text')?.value || '';
  const jobDescription = document.getElementById('job-description')?.value || '';

  if (!state.selectedFile && (!resumeText || resumeText.trim().length < 40)) {
    showToast('Please upload a resume or paste at least 40 characters of resume text.', 'warning');
    return;
  }

  showLoading('Analyzing ATS compliance, keywords, and impact metrics...');

  try {
    let responseData;

    if (state.selectedFile) {
      // Multipart upload
      const formData = new FormData();
      formData.append('file', state.selectedFile);
      formData.append('job_description', jobDescription);
      formData.append('api_key', state.apiKey);
      formData.append('api_provider', state.apiProvider);

      const res = await fetch('/api/analyze', {
        method: 'POST',
        body: formData,
      });
      responseData = await res.json();
    } else {
      // JSON payload
      const res = await fetch('/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          resume_text: resumeText,
          job_description: jobDescription,
          api_key: state.apiKey,
          api_provider: state.apiProvider,
        }),
      });
      responseData = await res.json();
    }

    if (!responseData.success) {
      throw new Error(responseData.error || 'Analysis failed');
    }

    state.analysisData = responseData;
    renderResults(responseData);

    // Celebration confetti if score is high
    if (responseData.ats_score >= 80 && typeof confetti === 'function') {
      confetti({
        particleCount: 80,
        spread: 70,
        origin: { y: 0.6 }
      });
    }

    showToast('Analysis completed successfully!', 'success');
  } catch (err) {
    console.error(err);
    showToast(err.message || 'Error processing resume. Check format.', 'error');
  } finally {
    hideLoading();
  }
}

// Render Results to UI
function renderResults(data) {
  const resultsSection = document.getElementById('results-section');
  if (resultsSection) {
    resultsSection.classList.remove('hidden');
    resultsSection.scrollIntoView({ behavior: 'smooth' });
  }

  // Candidate Name & Subtitle
  const candidateName = document.getElementById('candidate-name');
  if (candidateName) {
    candidateName.textContent = data.contact_info.name || 'Candidate Resume';
  }

  const candidateSub = document.getElementById('candidate-sub');
  if (candidateSub) {
    const metaParts = [];
    if (data.contact_info.email) metaParts.push(data.contact_info.email);
    if (data.contact_info.phone) metaParts.push(data.contact_info.phone);
    metaParts.push(`${data.metadata.word_count} words`);
    candidateSub.textContent = metaParts.join(' • ');
  }

  // Detected Skills Badge
  const skillsChip = document.getElementById('detected-skills-chip');
  if (skillsChip) {
    skillsChip.textContent = `🎯 ${data.total_detected_skills || 0} Skills Detected`;
  }

  // Animate Overall ATS Score Gauge
  animateScoreGauge(data.ats_score, data.tier_color);

  // Grade & Tier Badges
  const gradeBadge = document.getElementById('score-grade-badge');
  if (gradeBadge) {
    gradeBadge.textContent = `Grade ${data.ats_grade}`;
  }

  const tierBadge = document.getElementById('score-tier-badge');
  if (tierBadge) {
    tierBadge.textContent = data.tier_label;
    tierBadge.style.color = data.tier_color;
  }

  // Render 6 Breakdown Bars
  renderBreakdownBars(data.breakdown);

  // Render Radar Chart
  renderRadarChart(data.breakdown);

  // Strengths & Improvements
  renderStrengthsAndImprovements(data.strengths, data.improvements);

  // Skills Taxonomy Cloud
  renderSkillsCloud(data.detected_skills);

  // Job Matcher Section
  renderJobMatch(data.job_match);

  // Bullet Points in Optimizer
  populateBulletSelect(data.bullet_points_sample);

  // Interview Questions
  renderInterviewQuestions(data.interview_questions);

  // Resume Inspector Raw Text
  const rawTextDisplay = document.getElementById('raw-text-display');
  if (rawTextDisplay) {
    rawTextDisplay.textContent = data.raw_text;
  }

  // Weak Points & Missing Skills (Kamzoriyan & Gaps)
  renderWeakPoints(data.weak_points);
  renderMissingSkillsTab(data.missing_domain_skills, data.job_match);

  // Contact Chips
  renderContactChips(data.contact_info);
}

// Gauge Animation
function animateScoreGauge(score, color) {
  const scoreText = document.getElementById('ats-score-text');
  const circleProgress = document.getElementById('ats-circle-progress');
  if (!circleProgress) return;

  const circumference = 2 * Math.PI * 52; // r=52 -> ~326.7
  circleProgress.style.strokeDasharray = circumference;
  
  // Set initial stroke
  circleProgress.style.stroke = color || '#6366f1';

  let current = 0;
  const target = score;
  const duration = 1200;
  const startTime = performance.now();

  function updateGauge(now) {
    const elapsed = now - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const easeProgress = 1 - Math.pow(1 - progress, 3); // cubic ease-out
    current = Math.round(target * easeProgress);

    if (scoreText) scoreText.textContent = current;

    const offset = circumference - (current / 100) * circumference;
    circleProgress.style.strokeDashoffset = offset;

    if (progress < 1) {
      requestAnimationFrame(updateGauge);
    }
  }

  requestAnimationFrame(updateGauge);
}

// Breakdown Progress Bars
function renderBreakdownBars(breakdown) {
  const container = document.getElementById('breakdown-bars-container');
  if (!container) return;

  container.innerHTML = '';

  for (const [key, item] of Object.entries(breakdown)) {
    const barEl = document.createElement('div');
    barEl.className = 'space-y-1.5';

    const getStatusColor = (pct) => {
      if (pct >= 80) return 'bg-emerald-500';
      if (pct >= 60) return 'bg-indigo-500';
      if (pct >= 40) return 'bg-amber-500';
      return 'bg-rose-500';
    };

    barEl.innerHTML = `
      <div class="flex items-center justify-between text-xs font-semibold">
        <span class="text-slate-700 dark:text-slate-300">${item.title}</span>
        <span class="text-slate-900 dark:text-slate-100 font-bold">${item.score} / ${item.max} (${item.percentage}%)</span>
      </div>
      <div class="h-2 w-full bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
        <div class="h-full ${getStatusColor(item.percentage)} rounded-full transition-all duration-1000 ease-out" style="width: 0%" data-target-width="${item.percentage}%"></div>
      </div>
      <p class="text-[11px] text-slate-500 dark:text-slate-400 truncate">${item.feedback[0] || ''}</p>
    `;
    container.appendChild(barEl);
  }

  // Animate bar width
  setTimeout(() => {
    container.querySelectorAll('[data-target-width]').forEach((el) => {
      el.style.width = el.getAttribute('data-target-width');
    });
  }, 100);
}

// Chart.js Radar Visualization
function renderRadarChart(breakdown) {
  const canvas = document.getElementById('atsRadarChart');
  if (!canvas || typeof Chart === 'undefined') return;

  const isDark = state.theme === 'dark';
  const gridColor = isDark ? 'rgba(148, 163, 184, 0.2)' : 'rgba(148, 163, 184, 0.3)';
  const labelColor = isDark ? '#cbd5e1' : '#475569';

  const labels = Object.values(breakdown).map((b) => b.title.split(' ')[0]);
  const scores = Object.values(breakdown).map((b) => b.percentage);

  if (state.chartInstance) {
    state.chartInstance.destroy();
  }

  state.chartInstance = new Chart(canvas, {
    type: 'radar',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'ATS Compliance (%)',
          data: scores,
          backgroundColor: 'rgba(99, 102, 241, 0.25)',
          borderColor: '#6366f1',
          pointBackgroundColor: '#818cf8',
          pointBorderColor: '#ffffff',
          pointHoverBackgroundColor: '#ffffff',
          pointHoverBorderColor: '#6366f1',
          borderWidth: 2,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        r: {
          angleLines: { color: gridColor },
          grid: { color: gridColor },
          pointLabels: {
            color: labelColor,
            font: { family: 'Plus Jakarta Sans', size: 11, weight: '600' },
          },
          ticks: { display: false, min: 0, max: 100, stepSize: 25 },
          suggestedMin: 0,
          suggestedMax: 100,
        },
      },
      plugins: {
        legend: { display: false },
      },
    },
  });
}

// Strengths and Improvements
function renderStrengthsAndImprovements(strengths, improvements) {
  const strengthsContainer = document.getElementById('strengths-container');
  const improvementsContainer = document.getElementById('improvements-container');

  if (strengthsContainer) {
    strengthsContainer.innerHTML = strengths
      .map(
        (s) => `
      <li class="flex items-start text-xs sm:text-sm text-slate-700 dark:text-slate-300">
        <svg class="w-4 h-4 text-emerald-500 mr-2 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
        </svg>
        <span>${s}</span>
      </li>`
      )
      .join('');
  }

  if (improvementsContainer) {
    improvementsContainer.innerHTML = improvements
      .map(
        (i) => `
      <li class="flex items-start text-xs sm:text-sm text-slate-700 dark:text-slate-300">
        <svg class="w-4 h-4 text-amber-500 mr-2 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <span>${i}</span>
      </li>`
      )
      .join('');
  }
}

// Skills Cloud
function renderSkillsCloud(skillsDict) {
  const container = document.getElementById('skills-cloud-container');
  if (!container) return;

  container.innerHTML = '';
  const entries = Object.entries(skillsDict);

  if (entries.length === 0) {
    container.innerHTML = `<p class="text-xs text-slate-400">No recognizable industry skills detected.</p>`;
    return;
  }

  entries.forEach(([category, skills]) => {
    const catBlock = document.createElement('div');
    catBlock.className = 'space-y-2';

    const tagsHtml = skills
      .map(
        (sk) => `
      <span class="inline-flex items-center px-2.5 py-1 rounded-md text-xs font-medium bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-200 border border-slate-200 dark:border-slate-700">
        ${sk}
      </span>
    `
      )
      .join('');

    catBlock.innerHTML = `
      <h4 class="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">${category}</h4>
      <div class="flex flex-wrap gap-1.5">${tagsHtml}</div>
    `;
    container.appendChild(catBlock);
  });
}

// Job Match Section
function renderJobMatch(jd) {
  const matchPct = document.getElementById('jd-match-percentage');
  const matchedContainer = document.getElementById('jd-matched-keywords');
  const missingContainer = document.getElementById('jd-missing-keywords');
  const recoContainer = document.getElementById('jd-recommendations');

  if (matchPct) matchPct.textContent = `${jd.match_percentage}%`;

  if (matchedContainer) {
    if (jd.matched_keywords && jd.matched_keywords.length > 0) {
      matchedContainer.innerHTML = jd.matched_keywords
        .map(
          (k) => `
        <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800">
          ✓ ${k}
        </span>
      `
        )
        .join('');
    } else {
      matchedContainer.innerHTML = `<span class="text-xs text-slate-400">No matched keywords</span>`;
    }
  }

  if (missingContainer) {
    if (jd.missing_keywords && jd.missing_keywords.length > 0) {
      missingContainer.innerHTML = jd.missing_keywords
        .map(
          (k) => `
        <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold bg-amber-50 text-amber-700 dark:bg-amber-950/60 dark:text-amber-300 border border-amber-200 dark:border-amber-800">
          + ${k}
        </span>
      `
        )
        .join('');
    } else {
      missingContainer.innerHTML = `<span class="text-xs text-slate-400">No major missing keywords identified</span>`;
    }
  }

  if (recoContainer) {
    recoContainer.innerHTML = (jd.recommendations || [])
      .map(
        (r) => `
      <p class="text-xs sm:text-sm text-slate-600 dark:text-slate-300 flex items-start">
        <span class="text-indigo-500 mr-2 font-bold">•</span> ${r}
      </p>
    `
      )
      .join('');
  }
}

// Bullet Optimizer Setup
function populateBulletSelect(bullets) {
  const select = document.getElementById('bullet-select');
  const input = document.getElementById('custom-bullet-input');
  if (!select) return;

  select.innerHTML = '<option value="">-- Choose a bullet point from your resume --</option>';

  (bullets || []).forEach((b, idx) => {
    const opt = document.createElement('option');
    opt.value = b;
    opt.textContent = b.length > 70 ? b.substring(0, 67) + '...' : b;
    select.appendChild(opt);
  });

  select.onchange = () => {
    if (select.value && input) {
      input.value = select.value;
    }
  };

  // Pre-fill with first bullet if available
  if (bullets && bullets.length > 0 && input) {
    input.value = bullets[0];
  }
}

async function runBulletOptimizer() {
  const input = document.getElementById('custom-bullet-input');
  const bullet = input?.value?.trim();
  const resultsContainer = document.getElementById('optimizer-results');

  if (!bullet) {
    showToast('Please type or select a bullet point to optimize.', 'warning');
    return;
  }

  if (resultsContainer) {
    resultsContainer.innerHTML = `
      <div class="p-8 text-center text-slate-400 animate-pulse">
        <svg class="w-8 h-8 mx-auto mb-2 text-indigo-500 animate-spin" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
        </svg>
        Applying Google XYZ & STAR re-writing formulas...
      </div>
    `;
  }

  try {
    const res = await fetch('/api/optimize-bullet', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        bullet: bullet,
        role: state.analysisData?.contact_info?.name || 'Software Engineer',
        api_key: state.apiKey,
        api_provider: state.apiProvider,
      }),
    });
    const data = await res.json();
    if (data.success && resultsContainer) {
      renderOptimizerVariations(data.data);
    }
  } catch (err) {
    if (resultsContainer) {
      resultsContainer.innerHTML = `<p class="text-rose-500 text-sm">Optimization failed: ${err.message}</p>`;
    }
  }
}

function renderOptimizerVariations(optData) {
  const container = document.getElementById('optimizer-results');
  if (!container) return;

  const variationsHtml = optData.variations
    .map(
      (v, i) => `
    <div class="p-4 rounded-xl border border-slate-200 dark:border-slate-700 bg-white/70 dark:bg-slate-800/80 space-y-3 relative group transition hover:border-indigo-400">
      <div class="flex items-center justify-between">
        <span class="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-bold uppercase tracking-wider bg-indigo-50 text-indigo-600 dark:bg-indigo-950 dark:text-indigo-300">
          ${v.tag || 'Optimized'}
        </span>
        <button onclick="copyToClipboard('${escapeJsString(v.text)}', this)" class="text-xs text-slate-500 hover:text-indigo-600 dark:hover:text-indigo-400 flex items-center gap-1">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/></svg>
          Copy
        </button>
      </div>
      <p class="text-sm font-medium text-slate-900 dark:text-slate-100 leading-relaxed">${v.text}</p>
      <div class="text-[11px] text-slate-500 dark:text-slate-400 border-t border-slate-100 dark:border-slate-700/60 pt-2">
        <span class="font-semibold text-slate-700 dark:text-slate-300">Methodology:</span> ${v.framework}
      </div>
    </div>
  `
    )
    .join('');

  container.innerHTML = `
    <div class="space-y-3">
      <div class="flex items-center justify-between text-xs text-slate-500 mb-1">
        <span>Engine: <strong class="text-indigo-500">${optData.engine}</strong></span>
        <span>Theme: <strong>${optData.theme_detected}</strong></span>
      </div>
      ${variationsHtml}
    </div>
  `;
}

// Interview Questions
function renderInterviewQuestions(questions) {
  const container = document.getElementById('interview-questions-container');
  if (!container) return;

  if (!questions || questions.length === 0) {
    container.innerHTML = `<p class="text-sm text-slate-400">No questions generated yet.</p>`;
    return;
  }

  container.innerHTML = questions
    .map(
      (q, idx) => `
    <div class="rounded-xl border border-slate-200 dark:border-slate-700 bg-white/70 dark:bg-slate-800/80 p-4 space-y-3">
      <div class="flex items-center justify-between">
        <span class="text-[11px] font-bold uppercase tracking-wider text-indigo-600 dark:text-indigo-400 bg-indigo-50 dark:bg-indigo-950 px-2 py-0.5 rounded">
          ${q.category}
        </span>
        <span class="text-xs text-slate-400">Question ${idx + 1}</span>
      </div>
      <h4 class="text-sm sm:text-base font-semibold text-slate-900 dark:text-slate-100">
        "${q.question}"
      </h4>
      <div class="space-y-2 text-xs pt-1">
        <div class="p-2.5 rounded-lg bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-300">
          <span class="font-bold text-slate-900 dark:text-slate-100">🎯 What Interviewers Look For:</span> ${q.what_they_test}
        </div>
        <div class="p-2.5 rounded-lg bg-emerald-50/70 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800/60 text-emerald-800 dark:text-emerald-200">
          <span class="font-bold">💡 Recommended STAR Strategy:</span> ${q.star_guide}
        </div>
      </div>
    </div>
  `
    )
    .join('');
}

// Contact Chips
function renderContactChips(contact) {
  const container = document.getElementById('contact-chips-container');
  if (!container) return;

  container.innerHTML = '';
  const items = [
    { label: 'Email', val: contact.email, icon: '✉' },
    { label: 'Phone', val: contact.phone, icon: '📞' },
    { label: 'LinkedIn', val: contact.linkedin, icon: '🔗' },
    { label: 'GitHub', val: contact.github, icon: '🐙' },
  ];

  items.forEach((item) => {
    const chip = document.createElement('div');
    chip.className = `inline-flex items-center px-3 py-1.5 rounded-lg text-xs font-medium border ${
      item.val
        ? 'bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-950/60 dark:text-emerald-300 dark:border-emerald-800'
        : 'bg-rose-50 text-rose-700 border-rose-200 dark:bg-rose-950/60 dark:text-rose-300 dark:border-rose-800'
    }`;
    chip.innerHTML = `${item.icon} <span class="ml-1.5 font-bold">${item.label}:</span> <span class="ml-1 truncate max-w-[150px]">${item.val || 'Missing'}</span>`;
    container.appendChild(chip);
  });
}

// Tab Switching
function switchTab(tabId) {
  state.currentTab = tabId;
  document.querySelectorAll('.tab-btn').forEach((btn) => {
    if (btn.getAttribute('data-tab') === tabId) {
      btn.classList.add('border-indigo-600', 'text-indigo-600', 'dark:border-indigo-400', 'dark:text-indigo-400');
      btn.classList.remove('border-transparent', 'text-slate-500', 'hover:text-slate-700');
    } else {
      btn.classList.remove('border-indigo-600', 'text-indigo-600', 'dark:border-indigo-400', 'dark:text-indigo-400');
      btn.classList.add('border-transparent', 'text-slate-500', 'hover:text-slate-700');
    }
  });

  document.querySelectorAll('.tab-pane').forEach((pane) => {
    if (pane.id === `tab-${tabId}`) {
      pane.classList.remove('hidden');
    } else {
      pane.classList.add('hidden');
    }
  });

  // Re-render radar chart if overview selected
  if (tabId === 'overview' && state.chartInstance && state.analysisData) {
    state.chartInstance.resize();
  }
}

// Settings Modal
function openSettings() {
  const modal = document.getElementById('settings-modal');
  const keyInput = document.getElementById('api-key-input');
  const providerSelect = document.getElementById('api-provider-select');
  if (keyInput) keyInput.value = state.apiKey;
  if (providerSelect) providerSelect.value = state.apiProvider;
  if (modal) modal.classList.remove('hidden');
}

function closeSettings() {
  const modal = document.getElementById('settings-modal');
  if (modal) modal.classList.add('hidden');
}

function saveSettings() {
  const keyInput = document.getElementById('api-key-input');
  const providerSelect = document.getElementById('api-provider-select');
  if (keyInput) {
    state.apiKey = keyInput.value.trim();
    localStorage.setItem('gemini_api_key', state.apiKey);
  }
  if (providerSelect) {
    state.apiProvider = providerSelect.value;
    localStorage.setItem('api_provider', state.apiProvider);
  }
  closeSettings();
  showToast('Settings saved successfully', 'success');
}

// Helpers
function showLoading(msg = 'Processing...') {
  const overlay = document.getElementById('loading-overlay');
  const msgEl = document.getElementById('loading-text');
  if (msgEl) msgEl.textContent = msg;
  if (overlay) overlay.classList.remove('hidden');
}

function hideLoading() {
  const overlay = document.getElementById('loading-overlay');
  if (overlay) overlay.classList.add('hidden');
}

function showToast(message, type = 'info') {
  const toast = document.createElement('div');
  const colors = {
    success: 'bg-emerald-600 text-white',
    warning: 'bg-amber-600 text-white',
    error: 'bg-rose-600 text-white',
    info: 'bg-indigo-600 text-white',
  };

  toast.className = `fixed bottom-5 right-5 z-50 px-4 py-3 rounded-xl shadow-2xl text-xs sm:text-sm font-medium flex items-center gap-2 transform transition-all duration-300 translate-y-8 opacity-0 ${colors[type] || colors.info}`;
  toast.innerHTML = `<span>${message}</span>`;
  document.body.appendChild(toast);

  setTimeout(() => {
    toast.classList.remove('translate-y-8', 'opacity-0');
  }, 10);

  setTimeout(() => {
    toast.classList.add('translate-y-8', 'opacity-0');
    setTimeout(() => toast.remove(), 300);
  }, 3200);
}

function copyToClipboard(text, btn) {
  navigator.clipboard.writeText(text).then(() => {
    if (btn) {
      const orig = btn.innerHTML;
      btn.innerHTML = '✓ Copied!';
      btn.classList.add('text-emerald-500');
      setTimeout(() => {
        btn.innerHTML = orig;
        btn.classList.remove('text-emerald-500');
      }, 1500);
    }
  });
}
window.copyToClipboard = copyToClipboard;

function escapeJsString(str) {
  return (str || '')
    .replace(/\\/g, '\\\\')
    .replace(/'/g, "\\'")
    .replace(/"/g, '&quot;')
    .replace(/\n/g, ' ');
}

function resetAll() {
  clearSelectedFile();
  const resumeTextEl = document.getElementById('resume-text');
  const jdTextEl = document.getElementById('job-description');
  if (resumeTextEl) resumeTextEl.value = '';
  if (jdTextEl) jdTextEl.value = '';
  const resultsSection = document.getElementById('results-section');
  if (resultsSection) resultsSection.classList.add('hidden');
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Render Weak Points & Vulnerabilities (Kamzoriyan)
function renderWeakPoints(weakPoints) {
  const container = document.getElementById('weak-points-container');
  const counter = document.getElementById('weak-points-counter');
  if (!container) return;

  if (counter) {
    const criticalCount = (weakPoints || []).filter(w => w.severity === 'CRITICAL').length;
    counter.textContent = `${(weakPoints || []).length} Weaknesses (${criticalCount} Critical)`;
  }

  if (!weakPoints || weakPoints.length === 0) {
    container.innerHTML = `
      <div class="p-6 rounded-xl bg-emerald-950/30 border border-emerald-800 text-center">
        <p class="text-sm font-semibold text-emerald-300">🎉 No major weak points found! Your resume passes standard ATS benchmarks.</p>
      </div>`;
    return;
  }

  container.innerHTML = weakPoints.map((wp) => {
    const isCritical = wp.severity === 'CRITICAL';
    const badgeColor = isCritical 
      ? 'bg-rose-500/10 text-rose-400 border-rose-500/20' 
      : (wp.severity === 'MODERATE' ? 'bg-amber-500/10 text-amber-400 border-amber-500/20' : 'bg-blue-500/10 text-blue-400 border-blue-500/20');
    
    return `
      <div class="rounded-xl border border-slate-200 dark:border-slate-800 bg-white/70 dark:bg-slate-900/80 p-5 space-y-3.5 shadow-sm">
        <div class="flex flex-wrap items-center justify-between gap-2">
          <div class="flex items-center gap-2">
            <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-[11px] font-extrabold uppercase tracking-wider border ${badgeColor}">
              ${wp.severity_label || wp.severity}
            </span>
            <span class="text-xs font-bold text-slate-400">${wp.category}</span>
          </div>
          <span class="text-xs font-bold text-rose-400">${wp.impact}</span>
        </div>

        <h4 class="text-sm sm:text-base font-extrabold text-slate-900 dark:text-slate-100">
          ${wp.title}
        </h4>

        <div class="p-3 rounded-lg bg-rose-50/70 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-900/60 text-xs text-rose-800 dark:text-rose-200 space-y-1">
          <span class="font-bold">❌ Kamzori / Identified Weakness:</span>
          <p class="leading-relaxed">${wp.issue}</p>
        </div>

        <div class="p-3 rounded-lg bg-emerald-50/70 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-900/60 text-xs text-emerald-800 dark:text-emerald-200 space-y-1">
          <span class="font-bold">💡 How to Fix This (Hal):</span>
          <p class="leading-relaxed">${wp.how_to_fix}</p>
        </div>

        ${wp.example ? `
          <div class="p-3 rounded-lg bg-slate-100 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-[11px] font-mono text-slate-700 dark:text-slate-300">
            <span class="font-bold text-indigo-400 block mb-1">📝 Example:</span>
            ${wp.example}
          </div>
        ` : ''}
      </div>
    `;
  }).join('');
}

// Render Missing Skills
function renderMissingSkillsTab(missingBenchmarks, jd) {
  const jdContainer = document.getElementById('tab-jd-missing-container');
  const domainContainer = document.getElementById('tab-domain-missing-container');
  const counter = document.getElementById('missing-skills-counter');

  const hasJd = jd && jd.has_jd;
  const jdMissingCount = hasJd && jd.missing_keywords ? jd.missing_keywords.length : 0;

  if (counter) {
    if (hasJd) {
      counter.textContent = `${jdMissingCount} Missing from Job Description`;
      counter.className = `text-xs px-2.5 py-1 rounded-full font-bold border ${jdMissingCount > 0 ? 'bg-rose-500/10 text-rose-400 border-rose-500/20' : 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'}`;
    } else {
      counter.textContent = "No Job Description Provided";
      counter.className = "text-xs px-2.5 py-1 rounded-full font-medium border bg-slate-800 text-slate-400 border-slate-700";
    }
  }

  // JD Missing Section
  if (jdContainer) {
    if (hasJd) {
      if (jd.missing_keywords && jd.missing_keywords.length > 0) {
        const badges = jd.missing_keywords.map(k => `
          <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-rose-50 text-rose-700 dark:bg-rose-950/60 dark:text-rose-300 border border-rose-200 dark:border-rose-800">
            + ${k}
          </span>
        `).join('');
        jdContainer.innerHTML = `
          <div class="flex flex-wrap gap-2 mb-2">${badges}</div>
          <p class="text-xs text-slate-400">💡 <strong>How to Fix:</strong> These skills are requested in the job description but not detected in your resume. Add them naturally into your bullet points or skills list to improve your ATS match score.</p>
        `;
      } else {
        jdContainer.innerHTML = `<p class="text-xs text-emerald-400 font-semibold">🎉 100% Keyword Match! All skills required in this job description were found in your resume.</p>`;
      }
    } else {
      jdContainer.innerHTML = `
        <div class="p-4 rounded-xl bg-slate-950/60 border border-slate-800 text-slate-400 text-xs leading-relaxed">
          ℹ️ <strong>No Job Description provided yet.</strong> Paste a target Job Description in the form above to compare required skills against your resume and see genuinely missing skills.
        </div>
      `;
    }
  }

  // Domain Benchmarks Missing
  if (domainContainer) {
    if (!missingBenchmarks || missingBenchmarks.length === 0) {
      domainContainer.innerHTML = `<p class="text-xs text-emerald-400 font-semibold">✅ Your resume covers all core 2026 industry benchmark skills for your domain.</p>`;
    } else {
      domainContainer.innerHTML = missingBenchmarks.map(item => `
        <div class="p-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-white/60 dark:bg-slate-900/60 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div class="space-y-1">
            <div class="flex items-center gap-2">
              <span class="font-bold text-sm text-slate-900 dark:text-slate-100">➕ ${item.skill}</span>
              <span class="text-[10px] font-extrabold uppercase px-2 py-0.5 rounded ${item.importance === 'HIGH' ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20' : 'bg-amber-500/10 text-amber-400 border border-amber-500/20'}">
                ${item.importance} PRIORITY
              </span>
              <span class="text-xs text-slate-400">(${item.category})</span>
            </div>
            <p class="text-xs text-slate-600 dark:text-slate-300">${item.reason}</p>
          </div>
          <div class="text-[11px] font-medium text-indigo-400 bg-indigo-500/10 px-3 py-1.5 rounded-lg border border-indigo-500/20 whitespace-nowrap">
            ${item.suggested_placement}
          </div>
        </div>
      `).join('');
    }
  }
}

