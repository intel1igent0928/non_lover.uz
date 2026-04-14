// Register GSAP ScrollTrigger
gsap.registerPlugin(ScrollTrigger);

// Global State
const API_BASE = "/api";
let storyProgressTl;
let currentStoryIndex = 0;
let currentCategory = "";
let categoryData = {};
let animationsStarted = false;
let isFetching = false;
let isAppInitialized = false;
let allCategories = []; // List of category objects

// ---------------------------------------------------------
// Helper: Split Text
// ---------------------------------------------------------
function prepareTextReveal(selector) {
    const elements = document.querySelectorAll(selector);
    elements.forEach(el => {
        try {
            const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, null, false);
            const textNodes = [];
            let node;
            while (node = walker.nextNode()) {
                if (node.nodeValue.trim() !== '') textNodes.push(node);
            }

            textNodes.forEach(textNode => {
                if (!textNode.parentNode) return;
                const words = textNode.nodeValue.split(/(\s+)/);
                const fragment = document.createDocumentFragment();
                words.forEach(word => {
                    if (word.trim().length > 0) {
                        const span = document.createElement('span');
                        span.className = 'gsap-word';
                        span.style.display = 'inline-block';
                        span.style.willChange = 'transform, opacity';
                        span.textContent = word;
                        fragment.appendChild(span);
                    } else {
                        fragment.appendChild(document.createTextNode(word));
                    }
                });
                textNode.parentNode.replaceChild(fragment, textNode);
            });
        } catch (e) {
            console.error("Text splitting failed:", e);
        }
    });
}

// ---------------------------------------------------------
// Data Fetching & UI Update
// ---------------------------------------------------------
async function startApp() {
    if (isFetching) return;
    isFetching = true;

    try {
        console.log("Fetching platform data...");
        const [galleryRes, contentRes, linksRes, bannerRes, featuresRes, socialRes] = await Promise.all([
            fetch(`${API_BASE}/gallery/`),
            fetch(`${API_BASE}/content/`),
            fetch(`${API_BASE}/splash-links/`),
            fetch(`${API_BASE}/banner/`),
            fetch(`${API_BASE}/features/`),
            fetch(`${API_BASE}/social-links/`)
        ]);

        const galleries = await galleryRes.json();
        const contentData = await contentRes.json();
        const links = await linksRes.json();
        const banners = await bannerRes.json();
        const features = await featuresRes.json();
        const socialLinks = await socialRes.json();

        allCategories = galleries;

        // 1. Update Banner (Hero)
        if (banners.length > 0) {
            const b = banners[0];
            const img1 = document.getElementById("banner-image-1");
            const img2 = document.getElementById("banner-image-2");
            const titleEl = document.querySelector("[data-content='hero_title']");
            const subTitleEl = document.querySelector("[data-content='hero_subtitle']");

            if (img1 && b.image_1) img1.src = b.image_1;
            if (img2 && b.image_2) img2.src = b.image_2;
            if (titleEl && b.title) titleEl.innerText = b.title;
            if (subTitleEl && b.subtitle) subTitleEl.innerText = b.subtitle;
        }

        // 2. Update Gallery
        const listContainer = document.querySelector(".stories-list");
        if (listContainer) {
            listContainer.innerHTML = "";
            galleries.forEach(cat => {
                categoryData[cat.name] = cat.items;
                const preview = document.createElement("div");
                preview.className = "story-preview";
                preview.dataset.category = cat.name;
                preview.innerHTML = `
                    <img src="${cat.thumbnail}" alt="${cat.label}">
                    <div class="story-ring"></div>
                    <span class="story-label">${cat.label}</span>
                `;
                listContainer.appendChild(preview);

                preview.addEventListener("click", () => {
                    document.body.style.overflow = "hidden";
                    currentCategory = cat.name;
                    openStoryModal(0);
                });
            });
        }

        // 2. Update Content Texts
        document.querySelectorAll("[data-content]").forEach(el => {
            const key = el.dataset.content;
            if (contentData[key]) el.innerText = contentData[key];
        });

        // 4. Update Course Features (Modules)
        const featureContainer = document.getElementById("curriculum-grid");
        if (featureContainer && features.length > 0) {
            featureContainer.innerHTML = "";
            features.forEach(f => {
                const item = document.createElement("div");
                item.className = "grid-item";
                item.innerHTML = `
                    <div class="icon-box">
                        ${f.icon ? `<img src="${f.icon}" alt="${f.title}">` : ''}
                    </div>
                    <h3>${f.title}</h3>
                `;
                featureContainer.appendChild(item);
            });
        }

        // 5. Update Splash Links
        const splashContainer = document.querySelector(".splash-links");
        if (splashContainer && links.length > 0) {
            splashContainer.innerHTML = "";
            links.forEach(link => {
                const a = document.createElement("a");
                a.href = link.url;
                a.className = `splash-btn btn-${link.icon_type}`;
                a.innerText = link.title;
                if (link.icon_type !== 'enter') a.target = "_blank";
                else a.id = "enter-course";
                splashContainer.appendChild(a);
            });
        }

        // 6. Update Footer Social Links
        const socialContainer = document.getElementById("social-links-footer");
        if (socialContainer && socialLinks.length > 0) {
            socialContainer.innerHTML = "";
            socialLinks.forEach(link => {
                const a = document.createElement("a");
                a.href = link.url;
                a.target = "_blank";
                a.className = `social-btn ${link.icon_type}-btn`;

                let iconSrc = "";
                if (link.icon_type === 'telegram') iconSrc = "telega.png";
                else if (link.icon_type === 'instagram') iconSrc = "insta.png";
                else if (link.icon_type === 'phone') iconSrc = "phone.png";

                a.innerHTML = `<img src="/static/assets/${iconSrc}" alt="${link.icon_type}">`;
                socialContainer.appendChild(a);
            });
        }

        // 4. Initialize UI Sections after data is ready
        initSplashUI();
        initGalleryUI();

    } catch (e) {
        console.error("Initialization failed:", e);
        // Fallback: still show splash if API fails
        initSplashUI();
        initGalleryUI();
    }
}

// ---------------------------------------------------------
// UI Initialization
// ---------------------------------------------------------
function initSplashUI() {
    const overlay = document.getElementById("splash-overlay");
    const enterBtn = document.getElementById("enter-course");
    const showSplashBtn = document.getElementById("show-splash-btn");

    // Splash Entrance Animation
    const tlSplash = gsap.timeline();
    tlSplash.from(".splash-logo", { y: -30, opacity: 0, duration: 1, ease: "power3.out" })
        .from(".splash-insta", { opacity: 0, duration: 0.8 }, "-=0.5")
        .from(".splash-btn", { y: 20, opacity: 0, duration: 0.8, stagger: 0.2, ease: "back.out(1.7)" }, "-=0.3");

    if (enterBtn) {
        enterBtn.addEventListener("click", (e) => {
            e.preventDefault();
            gsap.to(overlay, {
                y: "-100%", duration: 1.2, ease: "power4.inOut",
                onComplete: () => {
                    overlay.style.display = "none";
                    if (!animationsStarted) {
                        startMainAnimations();
                        animationsStarted = true;
                    }
                    if (showSplashBtn) showSplashBtn.classList.add("visible");
                }
            });
        });
    }

    if (showSplashBtn) {
        showSplashBtn.onclick = () => {
            showSplashBtn.classList.remove("visible");
            overlay.style.display = "flex";
            gsap.to(overlay, { y: "0%", duration: 0.8, ease: "power3.inOut" });
        };
    }
}

function initGalleryUI() {
    const modal = document.getElementById("story-modal");
    if (!modal) return;

    const closeBtn = modal.querySelector(".story-close");
    const nextBtn = modal.querySelector(".story-next");
    const prevBtn = modal.querySelector(".story-prev");
    const likeBtn = modal.querySelector(".like-btn");
    const shareBtn = modal.querySelector(".share-btn");

    closeBtn.onclick = closeStoryModal;
    nextBtn.onclick = (e) => { e.stopPropagation(); navigateStory(1); };
    prevBtn.onclick = (e) => { e.stopPropagation(); navigateStory(-1); };

    likeBtn.onclick = (e) => {
        e.stopPropagation();
        const story = categoryData[currentCategory][currentStoryIndex];
        handleLike(story.id);
    };

    shareBtn.onclick = (e) => {
        e.stopPropagation();
        const story = categoryData[currentCategory][currentStoryIndex];
        handleShare(story.id);
    };

    initSwipeHandlers();
}

function initSwipeHandlers() {
    const modal = document.getElementById("story-modal");
    if (!modal) return;

    modal.style.touchAction = 'none'; // Prevent browser gestures

    let startX = 0;
    let isDragging = false;

    // Touch events
    modal.addEventListener('touchstart', e => {
        startX = e.changedTouches[0].clientX;
    }, { passive: true });

    modal.addEventListener('touchend', e => {
        const endX = e.changedTouches[0].clientX;
        handleGesture(startX, endX);
    }, { passive: true });

    // Mouse events (for desktop testing)
    modal.addEventListener('mousedown', e => {
        startX = e.clientX;
        isDragging = true;
    });

    modal.addEventListener('mouseup', e => {
        if (!isDragging) return;
        const endX = e.clientX;
        handleGesture(startX, endX);
        isDragging = false;
    });

    modal.addEventListener('mouseleave', () => {
        isDragging = false;
    });

    function handleGesture(sX, eX) {
        const threshold = 50;
        const diff = eX - sX;

        if (Math.abs(diff) > threshold) {
            if (diff > 0) {
                console.log("Swipe Right -> Prev Category");
                navigateCategory(-1);
            } else {
                console.log("Swipe Left -> Next Category");
                navigateCategory(1);
            }
        }
    }
}

function navigateCategory(direction) {
    const currentIndex = allCategories.findIndex(cat => cat.name === currentCategory);
    let nextIndex = currentIndex + direction;

    if (nextIndex >= 0 && nextIndex < allCategories.length) {
        const modalContainer = document.querySelector(".story-image-container");

        // Animation Out
        gsap.to(modalContainer, {
            x: direction > 0 ? -100 : 100,
            opacity: 0,
            duration: 0.3,
            ease: "power2.in",
            onComplete: () => {
                currentCategory = allCategories[nextIndex].name;
                currentStoryIndex = 0;

                const stories = categoryData[currentCategory];
                renderProgressBars(stories.length);
                updateStoryView(0);

                // Animation In
                gsap.fromTo(modalContainer,
                    { x: direction > 0 ? 100 : -100, opacity: 0 },
                    { x: 0, opacity: 1, duration: 0.4, ease: "power2.out" }
                );
            }
        });
    } else {
        closeStoryModal();
    }
}

// ---------------------------------------------------------
// Story Actions
// ---------------------------------------------------------
function openStoryModal(index) {
    const modal = document.getElementById("story-modal");
    const stories = categoryData[currentCategory];
    if (!stories || !modal) return;

    renderProgressBars(stories.length);
    modal.style.display = "flex";
    gsap.fromTo(modal, { opacity: 0 }, { opacity: 1, duration: 0.4 });
    updateStoryView(index);
}

function renderProgressBars(count) {
    const container = document.querySelector(".story-progress-container");
    container.innerHTML = "";
    for (let i = 0; i < count; i++) {
        const bar = document.createElement("div");
        bar.className = "story-progress-bar";
        bar.innerHTML = '<div class="story-progress-fill"></div>';
        container.appendChild(bar);
    }
}

function updateStoryView(index) {
    const stories = categoryData[currentCategory];
    const storyImg = document.getElementById("story-image");
    const modal = document.getElementById("story-modal");

    if (index < 0) return navigateCategory(-1);
    if (index >= stories.length) return navigateCategory(1);

    currentStoryIndex = index;
    const story = stories[index];
    storyImg.src = story.image;

    // Reset like button state
    const likeBtn = modal.querySelector(".like-btn");
    likeBtn.classList.remove("liked");

    const fills = modal.querySelectorAll(".story-progress-fill");
    if (storyProgressTl) storyProgressTl.kill();

    fills.forEach((fill, i) => {
        if (i < index) gsap.set(fill, { width: "100%" });
        else if (i > index) gsap.set(fill, { width: "0%" });
        else gsap.set(fill, { width: "0%" });
    });

    storyProgressTl = gsap.to(fills[index], {
        width: "100%", duration: 5, ease: "none",
        onComplete: () => updateStoryView(currentStoryIndex + 1)
    });
}

async function handleLike(itemId) {
    console.log("Liking item:", itemId);
    try {
        const res = await fetch(`${API_BASE}/story-item/${itemId}/like/`, { method: 'POST' });
        console.log("Like response status:", res.status);
        const data = await res.json();
        console.log("Like data:", data);
        if (data.status === 'liked') {
            triggerHeartAnimation();
            const likeBtn = document.querySelector('.like-btn');
            likeBtn.classList.add('liked');
        }
    } catch (e) {
        console.error("Like failed:", e);
    }
}

async function handleShare(itemId) {
    console.log("Sharing item:", itemId);
    try {
        const res = await fetch(`${API_BASE}/story-item/${itemId}/share/`, { method: 'POST' });
        console.log("Share response status:", res.status);
        const story = categoryData[currentCategory][currentStoryIndex];
        const shareData = {
            title: 'Zakvaskali Non',
            text: 'Haqiqiy zakvaskali non tayyorlashni o`rganing!',
            url: window.location.origin + story.image
        };
        if (navigator.share) {
            await navigator.share(shareData);
        } else {
            await navigator.clipboard.writeText(shareData.url);
            alert("Havola nusxalandi!");
        }
    } catch (e) {
        console.error("Share failed:", e);
    }
}

function triggerHeartAnimation() {
    const heart = document.querySelector('.big-heart');
    if (!heart) return;
    gsap.fromTo(heart,
        { scale: 0, opacity: 0 },
        {
            scale: 1, opacity: 1, duration: 0.4, ease: "back.out(1.7)", onComplete: () => {
                gsap.to(heart, { scale: 0, opacity: 0, duration: 0.3, delay: 0.8 });
            }
        }
    );
}

function navigateStory(direction) {
    updateStoryView(currentStoryIndex + direction);
}

function closeStoryModal() {
    const modal = document.getElementById("story-modal");
    document.body.style.overflow = "";
    gsap.to(modal, {
        opacity: 0, duration: 0.3, onComplete: () => {
            modal.style.display = "none";
            if (storyProgressTl) storyProgressTl.kill();
        }
    });
}

// ---------------------------------------------------------
// Main Animations
// ---------------------------------------------------------
function startMainAnimations() {
    gsap.to(".mobile-container", { opacity: 1, duration: 0.8, ease: "power2.out" });

    // Prepare all text for animation
    prepareTextReveal(".main-title, .hero-text, .section-title, .ticket-box p, .grid-item h3, .step-content h3, .step-content p, .format-card h3, .format-card p, .price-box h2");

    // 1. Hero Section
    const tlHero = gsap.timeline();
    tlHero.from("header .logo-cursive", { y: -20, opacity: 0, duration: 1.0, ease: "power2.out" })
        .from("header .main-title .gsap-word", { y: -20, opacity: 0, duration: 1.0, ease: "back.out(1.5)", stagger: 0.1 }, "-=0.6")
        .from(".hero-text .gsap-word", { y: 30, opacity: 0, duration: 1.2, ease: "power3.out", stagger: 0.08 }, "-=0.6")
        .from(".hero-images img", { y: 50, opacity: 0, scale: 0.9, duration: 1.2, stagger: 0.1, ease: "power2.out" }, "-=1.0")
        .from(".hero-btn", { scale: 0.8, opacity: 0, duration: 1.0, ease: "back.out(1.5)" }, "-=0.6");

    // 2. About Section
    const tlAbout = gsap.timeline({
        scrollTrigger: { trigger: ".about-course", start: "top 60%", toggleActions: "play none none reverse" }
    });
    tlAbout.from(".course-label", { scale: 0, rotation: -10, opacity: 0, duration: 0.7, ease: "back.out(1.5)" })
        .from(".ticket-box", { y: 30, opacity: 0, duration: 0.8, ease: "power2.out" }, "-=0.5")
        .from(".ticket-box p .gsap-word", { y: 15, opacity: 0, duration: 0.6, stagger: 0.03 }, "-=0.6")
        .from(".bullet", { x: -20, opacity: 0, duration: 0.6, stagger: 0.15 }, "-=0.4");

    // 3. Curriculum
    const tlCurriculum = gsap.timeline({
        scrollTrigger: { trigger: ".curriculum", start: "top 80%", toggleActions: "play none none reverse" }
    });
    tlCurriculum.from(".curriculum .section-title .gsap-word", { y: 20, opacity: 0, duration: 0.7, stagger: 0.05 })
        .from(".grid-item", { y: 30, opacity: 0, duration: 0.7, stagger: 0.15, ease: "power2.out" }, "-=0.4")
        .from(".grid-item h3 .gsap-word", { y: 10, opacity: 0, duration: 0.6, stagger: 0.04 }, "-=0.5")
        .from(".icon-box img", { scale: 0, opacity: 0, duration: 0.8, ease: "back.out(1.5)" }, "-=0.8");

    // 4. Steps
    gsap.utils.toArray(".timeline-item").forEach((item) => {
        const words = item.querySelectorAll(".gsap-word");
        const num = item.querySelector(".step-number");
        const img = item.querySelector(".step-illustration img");

        const tlStep = gsap.timeline({
            scrollTrigger: { trigger: item, start: "top 90%", toggleActions: "play none none reverse" }
        });

        tlStep.from(item, { y: 30, opacity: 0, duration: 0.7, ease: "power2.out" });
        if (num) tlStep.from(num, { scale: 0, rotation: -180, opacity: 0, duration: 0.7, ease: "back.out(2)" }, "-=0.5");
        if (words.length) tlStep.from(words, { y: 10, opacity: 0, duration: 0.6, stagger: 0.03, ease: "power2.out" }, "-=0.4");
        if (img) tlStep.from(img, { scale: 0.8, opacity: 0, duration: 1, ease: "power2.out" }, "-=0.6");
    });

    // 5. Format
    const tlFormat = gsap.timeline({
        scrollTrigger: { trigger: ".format", start: "top 80%", toggleActions: "play none none reverse" }
    });
    tlFormat.from(".format .section-title .gsap-word", { y: 20, opacity: 0, duration: 0.7, stagger: 0.05 })
        .from(".format-card", { y: 30, opacity: 0, duration: 0.7, stagger: 0.15, ease: "power2.out" }, "-=0.4")
        .from(document.querySelectorAll(".format-card .gsap-word"), { y: 10, opacity: 0, duration: 0.6, stagger: 0.03 }, "-=0.5");

    // 6. Pricing
    const tlPricing = gsap.timeline({
        scrollTrigger: { trigger: ".pricing", start: "top 85%", toggleActions: "play none none reverse" }
    });
    tlPricing.from(".price-box", { y: 30, scale: 0.98, opacity: 0, duration: 0.8, ease: "power2.out" })
        .from(".price-box h2 .gsap-word", { y: 15, opacity: 0, duration: 0.6, stagger: 0.05 }, "-=0.5")
        .fromTo(".old-price", { opacity: 0, y: 0, scale: 1.5 }, { opacity: 1, duration: 0.7, ease: "power2.out" }, "-=0.3")
        .to(".old-price", { "--strike-width": "104%", duration: 0.6, ease: "power2.inOut" })
        .to(".old-price", { y: -25, scale: 1, duration: 0.7, ease: "power2.inOut" }, "+=0.2")
        .fromTo(".new-price", { opacity: 0, y: 30, scale: 0.5 }, { opacity: 1, y: 15, scale: 1, duration: 0.8, ease: "back.out(1.7)" }, "-=0.4")
        .from(".btn-brown, .guarantee", { y: 15, opacity: 0, duration: 0.6, stagger: 0.1 }, "-=0.3");

    // Final Refresh
    ScrollTrigger.refresh();
}

// ---------------------------------------------------------
// Entry Point
// ---------------------------------------------------------
function init() {
    if (isAppInitialized) return;
    isAppInitialized = true;

    // Viewport fix
    const vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty('--vh', `${vh}px`);

    // Start Data Sync
    startApp();
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
