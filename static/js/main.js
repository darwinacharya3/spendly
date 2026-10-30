// main.js — students will add JavaScript here as features are built

(function () {
    var openBtn = document.getElementById("how-it-works-btn");
    var overlay = document.getElementById("video-modal-overlay");

    if (!openBtn || !overlay) {
        return;
    }

    var closeBtn = document.getElementById("video-modal-close");
    var iframe = document.getElementById("video-modal-iframe");

    // Fade the iframe in only once it has actually loaded, so a black
    // frame never flashes while the player is still starting up.
    iframe.addEventListener("load", function () {
        if (iframe.src) {
            iframe.classList.add("is-loaded");
        }
    });

    function openModal() {
        overlay.hidden = false;
        iframe.classList.remove("is-loaded");
        iframe.src = iframe.dataset.src;
        document.body.style.overflow = "hidden";

        // Force a reflow so the browser registers the "hidden" removal
        // before the opacity transition below starts, so it actually animates.
        void overlay.offsetWidth;
        overlay.classList.add("is-visible");
    }

    function closeModal() {
        overlay.classList.remove("is-visible");
        iframe.classList.remove("is-loaded");
        iframe.src = ""; // stop the video right away, before the fade-out finishes
        document.body.style.overflow = "";

        // Wait for the fade/scale transition (see CSS) to finish before
        // actually hiding the overlay, so closing looks smooth too.
        window.setTimeout(function () {
            overlay.hidden = true;
        }, 250);
    }

    openBtn.addEventListener("click", openModal);
    closeBtn.addEventListener("click", closeModal);

    // Close when clicking the overlay itself, not the modal content inside it.
    overlay.addEventListener("click", function (event) {
        if (event.target === overlay) {
            closeModal();
        }
    });

    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape" && !overlay.hidden) {
            closeModal();
        }
    });
})();
