document.addEventListener('DOMContentLoaded', function() {
    const noteCards = document.querySelectorAll('.note-card');

    noteCards.forEach(card => {
        const preview = card.querySelector('.note-content-preview');
        const fullContent = card.querySelector('.note-content-full');
        const showMoreLink = card.querySelector('.show-more-link');

        // Only show the link if the full content is actually longer than the preview
        if (fullContent && preview && fullContent.innerHTML.length > preview.innerHTML.length + 20) { // Heuristic check, adjust as needed
            showMoreLink.style.display = 'inline'; 
        } else if (showMoreLink) {
            showMoreLink.style.display = 'none';
        }

        if (showMoreLink && preview && fullContent) {
            showMoreLink.addEventListener('click', function(event) {
                event.preventDefault(); 

                if (fullContent.style.display === 'none') {
                    preview.style.display = 'none';
                    fullContent.style.display = 'block';
                    showMoreLink.textContent = 'Show Less';
                    card.classList.add('expanded'); 
                } else {
                    preview.style.display = 'block';
                    fullContent.style.display = 'none';
                    showMoreLink.textContent = 'Show More';
                    card.classList.remove('expanded');
                }
            });
        }
    });
});