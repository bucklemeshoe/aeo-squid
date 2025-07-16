// AEO Assessment Tool - Main JavaScript

// Configuration
const CONFIG = {
    API_BASE_URL: 'http://localhost:8001/api', // Adjust based on deployment
    ANALYSIS_POLL_INTERVAL: 2000, // 2 seconds
    MAX_POLL_ATTEMPTS: 300, // 10 minutes max (PageSpeed API can be slow)
    LOCAL_STORAGE_KEY: 'aeo_analysis'
};

// State management
let currentAnalysisId = null;
let pollInterval = null;
let pollAttempts = 0;

// DOM elements
const form = document.getElementById('analysis-form');
const urlInput = document.getElementById('website-url');
const emailInput = document.getElementById('email');
const privacyConsent = document.getElementById('privacy-consent');
const analyzeBtn = document.getElementById('analyze-btn');

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// Initialize application
function initializeApp() {
    setupEventListeners();
    checkExistingAnalysis();
    prefillDemoData(); // Remove in production
}

// Setup event listeners
function setupEventListeners() {
    // Form submission
    form.addEventListener('submit', handleFormSubmit);
    
    // URL input validation
    urlInput.addEventListener('blur', validateUrl);
    urlInput.addEventListener('input', clearErrors);
    
    // Email input validation
    emailInput.addEventListener('blur', validateEmail);
    emailInput.addEventListener('input', clearErrors);
    
    // Privacy consent
    privacyConsent.addEventListener('change', updateSubmitButton);
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Handle form submission
async function handleFormSubmit(e) {
    e.preventDefault();
    
    if (!validateForm()) {
        return;
    }
    
    const formData = {
        url: urlInput.value.trim(),
        email: emailInput.value.trim()
    };
    
    try {
        setLoadingState(true);
        
        // Submit analysis request
        const response = await fetch(`${CONFIG.API_BASE_URL}/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        if (result.analysis_id) {
            currentAnalysisId = result.analysis_id;
            saveAnalysisToStorage(result);
            
            // Track analytics
            trackEvent('analysis_started', {
                url: formData.url,
                analysis_id: result.analysis_id
            });
            
            // Redirect to loading page or show progress
            showAnalysisProgress();
            startPollingForResults();
        } else {
            throw new Error('No analysis ID received');
        }
        
    } catch (error) {
        console.error('Analysis submission error:', error);
        showError('Failed to start analysis. Please try again.');
        setLoadingState(false);
    }
}

// Validate form
function validateForm() {
    let isValid = true;
    
    // Clear previous errors
    clearErrors();
    
    // Validate URL
    if (!validateUrl()) {
        isValid = false;
    }
    
    // Validate email
    if (!validateEmail()) {
        isValid = false;
    }
    
    // Validate privacy consent
    if (!privacyConsent.checked) {
        showFieldError(privacyConsent, 'Please agree to the terms and privacy policy.');
        isValid = false;
    }
    
    return isValid;
}

// Validate URL
function validateUrl() {
    const url = urlInput.value.trim();
    
    if (!url) {
        showFieldError(urlInput, 'Please enter a website URL.');
        return false;
    }
    
    try {
        const urlObj = new URL(url);
        if (!['http:', 'https:'].includes(urlObj.protocol)) {
            showFieldError(urlInput, 'Please enter a valid HTTP or HTTPS URL.');
            return false;
        }
        
        // Basic domain validation
        if (!urlObj.hostname || urlObj.hostname.length < 3) {
            showFieldError(urlInput, 'Please enter a valid domain name.');
            return false;
        }
        
        return true;
    } catch (error) {
        showFieldError(urlInput, 'Please enter a valid website URL.');
        return false;
    }
}

// Validate email
function validateEmail() {
    const email = emailInput.value.trim();
    
    if (!email) {
        showFieldError(emailInput, 'Please enter an email address.');
        return false;
    }
    
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        showFieldError(emailInput, 'Please enter a valid email address.');
        return false;
    }
    
    return true;
}

// Show field error
function showFieldError(field, message) {
    field.classList.add('is-invalid');
    const feedback = field.parentElement.querySelector('.invalid-feedback');
    if (feedback) {
        feedback.textContent = message;
    }
}

// Clear all errors
function clearErrors() {
    document.querySelectorAll('.is-invalid').forEach(field => {
        field.classList.remove('is-invalid');
    });
}

// Update submit button state
function updateSubmitButton() {
    const isValid = urlInput.value.trim() && 
                   emailInput.value.trim() && 
                   privacyConsent.checked;
    
    analyzeBtn.disabled = !isValid;
}

// Set loading state
function setLoadingState(isLoading) {
    if (isLoading) {
        analyzeBtn.classList.add('loading');
        analyzeBtn.disabled = true;
        form.classList.add('loading');
    } else {
        analyzeBtn.classList.remove('loading');
        analyzeBtn.disabled = false;
        form.classList.remove('loading');
    }
}

// Show analysis progress
function showAnalysisProgress() {
    // Create progress modal or redirect to analysis page
    const progressModal = createProgressModal();
    document.body.appendChild(progressModal);
    
    // Show the modal with proper configuration
    const modal = new bootstrap.Modal(progressModal, {
        backdrop: 'static', // Prevent clicking outside to close
        keyboard: false     // Prevent ESC key from closing
    });
    modal.show();
    
    // Store modal reference globally for updates
    window.currentProgressModal = modal;
}

// Create progress modal
function createProgressModal() {
    const modalHTML = `
        <div class="modal fade" id="analysisProgressModal" tabindex="-1" aria-hidden="true">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header border-0">
                        <h5 class="modal-title">
                            <i class="fas fa-cogs text-primary me-2"></i>
                            Analyzing Your Website
                        </h5>
                        <small class="text-muted ms-auto">Analysis continues even if you close this window</small>
                    </div>
                    <div class="modal-body">
                        <div class="text-center mb-4">
                            <div class="spinner-border text-primary" role="status" style="width: 3rem; height: 3rem;">
                                <span class="visually-hidden">Loading...</span>
                            </div>
                        </div>
                        
                        <div class="progress mb-4" style="height: 8px;">
                            <div class="progress-bar progress-bar-striped progress-bar-animated" 
                                 role="progressbar" 
                                 style="width: 0%" 
                                 id="analysisProgress">
                            </div>
                        </div>
                        
                        <div id="progressSteps">
                            ${createProgressSteps()}
                        </div>
                        
                        <div class="alert alert-info mt-4">
                            <i class="fas fa-info-circle me-2"></i>
                            This usually takes 2-3 minutes. We're checking your website's performance, 
                            schema markup, content structure, and technical SEO.
                        </div>
                        
                        <div class="text-center">
                            <p class="text-muted mb-2">
                                <strong>Analysis ID:</strong> <code id="analysisIdDisplay">${currentAnalysisId}</code>
                            </p>
                            <small class="text-muted">
                                You can bookmark this page or we'll email you the results.
                            </small>
                        </div>
                    </div>
                    <div class="modal-footer border-0">
                        <button type="button" class="btn btn-outline-secondary" onclick="runInBackground()">
                            <i class="fas fa-minimize me-2"></i>
                            Minimize (Continue in Background)
                        </button>
                        <button type="button" class="btn btn-outline-danger" onclick="cancelAnalysis()">
                            <i class="fas fa-times me-2"></i>
                            Cancel Analysis
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    const modalElement = document.createElement('div');
    modalElement.innerHTML = modalHTML;
    return modalElement.firstElementChild;
}

// Create progress steps
function createProgressSteps() {
    const steps = [
        { icon: 'fas fa-globe', text: 'Fetching website content', id: 'step-fetch' },
        { icon: 'fas fa-tachometer-alt', text: 'Analyzing performance metrics', id: 'step-performance' },
        { icon: 'fas fa-code', text: 'Checking schema markup', id: 'step-schema' },
        { icon: 'fas fa-mobile-alt', text: 'Testing mobile optimization', id: 'step-mobile' },
        { icon: 'fas fa-chart-line', text: 'Generating recommendations', id: 'step-recommendations' }
    ];
    
    return steps.map(step => `
        <div class="progress-step" id="${step.id}">
            <div class="step-icon">
                <i class="${step.icon}"></i>
            </div>
            <span>${step.text}</span>
        </div>
    `).join('');
}

// Start polling for results
function startPollingForResults() {
    pollAttempts = 0;
    
    pollInterval = setInterval(async () => {
        pollAttempts++;
        
        try {
            const response = await fetch(`${CONFIG.API_BASE_URL}/analysis/${currentAnalysisId}`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const result = await response.json();
            
            // Update progress
            updateProgress(result);
            
            if (result.status === 'completed') {
                clearInterval(pollInterval);
                handleAnalysisComplete(result);
            } else if (result.status === 'failed') {
                clearInterval(pollInterval);
                handleAnalysisError(result.error || 'Analysis failed');
            } else if (pollAttempts >= CONFIG.MAX_POLL_ATTEMPTS) {
                clearInterval(pollInterval);
                handleAnalysisTimeout();
            }
            
        } catch (error) {
            console.error('Polling error:', error);
            
            if (pollAttempts >= CONFIG.MAX_POLL_ATTEMPTS) {
                clearInterval(pollInterval);
                handleAnalysisError('Connection timeout. Please check your results via email.');
            }
        }
    }, CONFIG.ANALYSIS_POLL_INTERVAL);
}

// Update progress
function updateProgress(result) {
    const progressBar = document.getElementById('analysisProgress');
    
    if (result.progress !== undefined) {
        // Update progress bar
        progressBar.style.width = `${result.progress}%`;
        
        // Update current step display
        if (result.current_step) {
            updateCurrentStepDisplay(result.current_step);
        }
        
        // Update step visual indicators based on progress
        updateProgressSteps(result.progress);
    }
}

// Update current step display
function updateCurrentStepDisplay(currentStep) {
    // Update or create a current step display
    let stepDisplay = document.getElementById('currentStepDisplay');
    if (!stepDisplay) {
        // Create the display element
        const progressDiv = document.querySelector('#analysisProgressModal .modal-body');
        const progressBar = document.querySelector('.progress');
        
        stepDisplay = document.createElement('div');
        stepDisplay.id = 'currentStepDisplay';
        stepDisplay.className = 'text-center text-muted mb-3';
        stepDisplay.style.minHeight = '20px';
        
        progressBar.insertAdjacentElement('afterend', stepDisplay);
    }
    
    stepDisplay.innerHTML = `<i class="fas fa-cog fa-spin me-2"></i>${currentStep}`;
}

// Update progress steps based on percentage
function updateProgressSteps(progressPercentage) {
    const steps = [
        { id: 'step-fetch', threshold: 10 },
        { id: 'step-performance', threshold: 25 },
        { id: 'step-schema', threshold: 50 },
        { id: 'step-mobile', threshold: 75 },
        { id: 'step-recommendations', threshold: 90 }
    ];
    
    steps.forEach(step => {
        const stepElement = document.getElementById(step.id);
        if (stepElement) {
            stepElement.classList.remove('active', 'completed');
            
            if (progressPercentage > step.threshold) {
                stepElement.classList.add('completed');
            } else if (progressPercentage >= step.threshold - 15) {
                stepElement.classList.add('active');
            }
        }
    });
}

// Handle analysis completion
function handleAnalysisComplete(result) {
    // Track analytics
    trackEvent('analysis_completed', {
        analysis_id: currentAnalysisId,
        overall_score: result.overall_score
    });
    
    // Save results to storage
    saveAnalysisToStorage(result);
    
    // Stop polling
    if (pollInterval) {
        clearInterval(pollInterval);
        pollInterval = null;
    }
    
    // If progress modal is still open, close it
    const progressModal = document.getElementById('analysisProgressModal');
    if (progressModal) {
        closeProgressModal();
    }
    
    // Show completion notification if modal was minimized
    showCompletionNotification();
    
    // Show results
    setTimeout(() => {
        showResults(result.results || result);
    }, 500); // Small delay for better UX
}

// Show completion notification
function showCompletionNotification() {
    const notificationHTML = `
        <div class="alert alert-success alert-dismissible fade show position-fixed" 
             style="top: 20px; right: 20px; z-index: 9999; max-width: 400px;" role="alert">
            <i class="fas fa-check-circle me-2"></i>
            <strong>Analysis Complete!</strong><br>
            <small>Your AEO assessment results are ready to view.</small>
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    const alertElement = document.createElement('div');
    alertElement.innerHTML = notificationHTML;
    document.body.appendChild(alertElement.firstElementChild);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        const alert = document.querySelector('.alert-success');
        if (alert && alert.textContent.includes('Analysis Complete')) {
            alert.remove();
        }
    }, 5000);
}

// Handle analysis error
function handleAnalysisError(errorMessage) {
    console.error('Analysis error:', errorMessage);
    
    // Track analytics
    trackEvent('analysis_failed', {
        analysis_id: currentAnalysisId,
        error: errorMessage
    });
    
    // Stop polling
    if (pollInterval) {
        clearInterval(pollInterval);
        pollInterval = null;
    }
    
    // Close progress modal if open
    const progressModal = document.getElementById('analysisProgressModal');
    if (progressModal) {
        closeProgressModal();
    }
    
    showError(`Analysis failed: ${errorMessage}`);
    setLoadingState(false);
}

// Handle analysis timeout
function handleAnalysisTimeout() {
    console.warn('Analysis timeout');
    
    // Track analytics
    trackEvent('analysis_timeout', {
        analysis_id: currentAnalysisId
    });
    
    // Stop polling
    if (pollInterval) {
        clearInterval(pollInterval);
        pollInterval = null;
    }
    
    // Close progress modal if open
    const progressModal = document.getElementById('analysisProgressModal');
    if (progressModal) {
        closeProgressModal();
    }
    
    showError('Analysis is taking longer than expected. We\'ll email you the results when ready.');
    setLoadingState(false);
}

// Show results
function showResults(result) {
    // Close progress modal
    closeProgressModal();
    
    // Reset loading state
    setLoadingState(false);
    
    // Create and show results dashboard
    const resultsModal = createResultsModal(result);
    document.body.appendChild(resultsModal);
    
    const modal = new bootstrap.Modal(resultsModal);
    modal.show();
    
    // Initialize charts and interactive elements
    setTimeout(() => {
        initializeResultsInteractivity(result);
    }, 300);
}

// Create results modal
function createResultsModal(result) {
    const modalHTML = `
        <div class="modal fade" id="resultsModal" tabindex="-1" aria-hidden="true">
            <div class="modal-dialog modal-xl">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i class="fas fa-chart-line text-primary me-2"></i>
                            AEO Analysis Results
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body" style="max-height: 80vh; overflow-y: auto;">
                        ${createResultsDashboard(result)}
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">
                            Close
                        </button>
                        <button type="button" class="btn btn-success" onclick="downloadPDF()">
                            <i class="fas fa-file-pdf me-2"></i>
                            Download PDF
                        </button>
                        <button type="button" class="btn btn-primary" onclick="contactForImplementation()">
                            <i class="fas fa-rocket me-2"></i>
                            Get Implementation Help
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    const modalElement = document.createElement('div');
    modalElement.innerHTML = modalHTML;
    return modalElement.firstElementChild;
}

// Create results dashboard
function createResultsDashboard(result) {
    return `
        <div class="row">
            <!-- Overall Score -->
            <div class="col-12 text-center mb-4">
                <div class="score-circle mx-auto" style="--score: ${result.overall_score}">
                    <div class="score-text">
                        <div class="score-number">${result.overall_score}</div>
                        <div class="score-label">Score</div>
                    </div>
                </div>
                <h3 class="mt-3">${getScoreDescription(result.overall_score)}</h3>
                <p class="text-muted">Your website's AI readiness score out of 100</p>
            </div>
            
            <!-- Category Scores -->
            <div class="col-12 mb-4">
                <h4 class="mb-3">Category Breakdown</h4>
                <div class="row g-3">
                    ${createCategoryCards(result.category_scores || {})}
                </div>
            </div>
            
            <!-- Recommendations -->
            <div class="col-12 mb-4">
                <h4 class="mb-3">Priority Recommendations</h4>
                ${createRecommendations(result.recommendations || [])}
            </div>
            
            <!-- Technical Details -->
            <div class="col-12">
                <h4 class="mb-3">Detailed Analysis</h4>
                ${createTechnicalDetails(result.detailed_results || {})}
            </div>
        </div>
    `;
}

// Get score description
function getScoreDescription(score) {
    if (score >= 80) return 'Excellent AI Readiness';
    if (score >= 65) return 'Good AI Readiness';
    if (score >= 45) return 'Fair AI Readiness';
    return 'Needs Improvement';
}

// Create category cards
function createCategoryCards(scores) {
    const categories = [
        { key: 'performance', name: 'Performance', icon: 'fas fa-tachometer-alt' },
        { key: 'schema', name: 'Schema Markup', icon: 'fas fa-code' },
        { key: 'content', name: 'Content Structure', icon: 'fas fa-comments' },
        { key: 'technical', name: 'Technical SEO', icon: 'fas fa-cogs' }
    ];
    
    // Ensure scores is an object
    const safeScores = scores || {};
    
    return categories.map(category => {
        const score = safeScores[category.key] || 0;
        const status = getStatusClass(score, 25);
        const percentage = (score / 25) * 100;
        
        return `
            <div class="col-md-6 col-lg-3">
                <div class="card category-card ${status}">
                    <div class="card-body">
                        <div class="d-flex align-items-center mb-2">
                            <i class="${category.icon} me-2"></i>
                            <h6 class="card-title mb-0">${category.name}</h6>
                        </div>
                        <div class="category-score ${status}">${score}/25</div>
                        <div class="category-progress">
                            <div class="category-progress-bar" style="width: ${percentage}%"></div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

// Get status class based on score
function getStatusClass(score, maxScore) {
    const percentage = (score / maxScore) * 100;
    if (percentage >= 80) return 'status-excellent';
    if (percentage >= 65) return 'status-good';
    if (percentage >= 45) return 'status-fair';
    return 'status-poor';
}

// Create recommendations
function createRecommendations(recommendations) {
    if (!recommendations.length) {
        return '<p class="text-muted">Great job! No major recommendations at this time.</p>';
    }
    
    return recommendations.slice(0, 5).map(rec => {
        // Handle both string and object recommendations
        if (typeof rec === 'string') {
            return `
                <div class="card recommendation-card mb-3">
                    <div class="card-body">
                        <div class="d-flex align-items-start mb-2">
                            <i class="fas fa-lightbulb text-warning me-3 mt-1"></i>
                            <p class="card-text mb-0">${rec}</p>
                        </div>
                    </div>
                </div>
            `;
        } else {
            // Handle detailed recommendation objects
            return `
                <div class="card recommendation-card ${rec.impact.toLowerCase()}-impact mb-3">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-start mb-2">
                            <h6 class="card-title mb-0">${rec.title}</h6>
                            <div>
                                <span class="badge impact-badge impact-${rec.impact.toLowerCase()}">${rec.impact} Impact</span>
                                <span class="badge difficulty-badge difficulty-${rec.difficulty.toLowerCase()}">${rec.difficulty}</span>
                            </div>
                        </div>
                        <p class="card-text text-muted">${rec.description}</p>
                        ${rec.action_items ? `
                            <ul class="list-unstyled mb-0">
                                ${rec.action_items.slice(0, 3).map(item => `<li><i class="fas fa-check text-success me-2"></i>${item}</li>`).join('')}
                            </ul>
                        ` : ''}
                    </div>
                </div>
            `;
        }
    }).join('');
}

// Create technical details
function createTechnicalDetails(details) {
    return `
        <div class="accordion" id="technicalDetailsAccordion">
            <div class="accordion-item">
                <h2 class="accordion-header">
                    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#technicalDetails">
                        <i class="fas fa-cogs me-2"></i>
                        View Technical Details
                    </button>
                </h2>
                <div id="technicalDetails" class="accordion-collapse collapse" data-bs-parent="#technicalDetailsAccordion">
                    <div class="accordion-body">
                        <pre class="bg-light p-3 rounded"><code>${JSON.stringify(details, null, 2)}</code></pre>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// Initialize results interactivity
function initializeResultsInteractivity(result) {
    // Animate score circle
    animateScoreCircle();
    
    // Animate progress bars
    animateProgressBars();
    
    // Add tooltips
    initializeTooltips();
}

// Animate score circle
function animateScoreCircle() {
    const scoreCircle = document.querySelector('.score-circle');
    if (scoreCircle) {
        scoreCircle.style.animation = 'scaleIn 0.8s ease-out';
    }
}

// Animate progress bars
function animateProgressBars() {
    const progressBars = document.querySelectorAll('.category-progress-bar');
    progressBars.forEach((bar, index) => {
        setTimeout(() => {
            bar.style.transition = 'width 1s ease-out';
            bar.style.width = bar.style.width; // Trigger animation
        }, index * 200);
    });
}

// Initialize tooltips
function initializeTooltips() {
    const tooltipElements = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltipElements.forEach(element => {
        new bootstrap.Tooltip(element);
    });
}

// Close progress modal (updated to NOT stop polling)
function closeProgressModal() {
    const modal = document.getElementById('analysisProgressModal');
    if (modal) {
        const bsModal = bootstrap.Modal.getInstance(modal);
        if (bsModal) {
            bsModal.hide();
        }
        modal.remove();
    }
    
    // Remove modal reference
    if (window.currentProgressModal) {
        delete window.currentProgressModal;
    }
    
    // DO NOT clear polling interval here - let analysis continue in background
    // Only clear it if explicitly cancelled or completed
}

// Run analysis in background (just hide modal, keep polling)
function runInBackground() {
    // Just hide the modal, don't stop polling
    const modal = document.getElementById('analysisProgressModal');
    if (modal && window.currentProgressModal) {
        window.currentProgressModal.hide();
    }
    
    // Show a small notification that analysis continues
    showBackgroundNotification();
}

// Show background notification
function showBackgroundNotification() {
    const notificationHTML = `
        <div class="alert alert-success alert-dismissible fade show position-fixed" 
             style="bottom: 20px; right: 20px; z-index: 9999; max-width: 350px;" role="alert">
            <i class="fas fa-check-circle me-2"></i>
            <strong>Analysis running in background</strong><br>
            <small>You'll see results when complete, or we'll email them to you.</small>
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    const alertElement = document.createElement('div');
    alertElement.innerHTML = notificationHTML;
    document.body.appendChild(alertElement.firstElementChild);
    
    // Auto-remove after 8 seconds
    setTimeout(() => {
        const alert = document.querySelector('.alert-success');
        if (alert) {
            alert.remove();
        }
    }, 8000);
}

// Cancel analysis completely
function cancelAnalysis() {
    if (confirm('Are you sure you want to cancel the analysis?')) {
        // Stop polling
        if (pollInterval) {
            clearInterval(pollInterval);
            pollInterval = null;
        }
        
        // Clear current analysis
        currentAnalysisId = null;
        
        // Remove from storage
        localStorage.removeItem(CONFIG.LOCAL_STORAGE_KEY);
        
        // Close modal
        closeProgressModal();
        
        // Reset form
        setLoadingState(false);
        
        // Track cancellation
        trackEvent('analysis_cancelled');
        
        showError('Analysis cancelled.');
    }
}

// Download PDF
function downloadPDF() {
    if (!currentAnalysisId) return;
    
    // Track analytics
    trackEvent('pdf_download', {
        analysis_id: currentAnalysisId
    });
    
    // Open PDF in new tab
    window.open(`${CONFIG.API_BASE_URL}/report/${currentAnalysisId}/pdf`, '_blank');
}

// Contact for implementation
function contactForImplementation() {
    // Track analytics
    trackEvent('contact_implementation', {
        analysis_id: currentAnalysisId
    });
    
    // Show contact form or redirect to contact page
    showContactForm();
}

// Show contact form
function showContactForm() {
    // Implementation depends on your contact system
    alert('Contact form would be implemented here. For now, please email us at contact@example.com');
}

// Show error message
function showError(message) {
    // Create and show error alert
    const alertHTML = `
        <div class="alert alert-danger alert-dismissible fade show position-fixed" 
             style="top: 20px; right: 20px; z-index: 9999;" role="alert">
            <i class="fas fa-exclamation-triangle me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    const alertElement = document.createElement('div');
    alertElement.innerHTML = alertHTML;
    document.body.appendChild(alertElement.firstElementChild);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        const alert = document.querySelector('.alert');
        if (alert) {
            alert.remove();
        }
    }, 5000);
}

// Save analysis to local storage
function saveAnalysisToStorage(analysis) {
    try {
        localStorage.setItem(CONFIG.LOCAL_STORAGE_KEY, JSON.stringify({
            ...analysis,
            timestamp: Date.now()
        }));
    } catch (error) {
        console.warn('Could not save to localStorage:', error);
    }
}

// Check for existing analysis
function checkExistingAnalysis() {
    try {
        const stored = localStorage.getItem(CONFIG.LOCAL_STORAGE_KEY);
        if (stored) {
            const analysis = JSON.parse(stored);
            
            // Check if less than 1 hour old
            if (Date.now() - analysis.timestamp < 3600000) {
                currentAnalysisId = analysis.analysis_id;
                
                        // If completed, show results
        if (analysis.status === 'completed') {
            showResults(analysis.results || analysis);
                } else if (analysis.status === 'processing') {
                    // Resume polling
                    showAnalysisProgress();
                    startPollingForResults();
                }
            }
        }
    } catch (error) {
        console.warn('Could not load from localStorage:', error);
    }
}

// Track analytics events
function trackEvent(eventName, parameters = {}) {
    // Google Analytics 4
    if (typeof gtag !== 'undefined') {
        gtag('event', eventName, parameters);
    }
    
    // Console log for development
    console.log('Analytics Event:', eventName, parameters);
}

// Prefill demo data (remove in production)
function prefillDemoData() {
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        urlInput.value = 'https://example.com';
        emailInput.value = 'demo@example.com';
        privacyConsent.checked = true;
        updateSubmitButton();
    }
}

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
} 