document.addEventListener('DOMContentLoaded', function() {
    // Select all elements with the class 'note-card'
    const noteCards = document.querySelectorAll('.note-card');

    noteCards.forEach(card => {
        const preview = card.querySelector('.note-content-preview');
        const fullContent = card.querySelector('.note-content-full');
        const showMoreLink = card.querySelector('.show-more-link');

        // --- Add logic here to determine initial visibility ---
        if (preview && fullContent && showMoreLink) {
            // Check if the full content is substantially longer than the preview
            // You might need to adjust this logic based on how your preview is generated
            // A simple check is if the full content exists and is different from the preview
            // or if the full content's text length exceeds a certain threshold.
            
            // Let's assume if fullContent has any text and is not just whitespace,
            // the 'Show More' link should potentially be visible.
            // A more robust check might compare text lengths or check for an ellipsis in the preview.
            
            const fullText = fullContent.textContent.trim();
            const previewText = preview.textContent.trim();

            // Simple check: If full content exists and is different from preview, show the link
            // You might need a more complex check if preview is just a truncated version of fullContent
            if (fullText && fullText !== previewText) {
                 // Ensure the link is visible initially if content is long
                 showMoreLink.style.display = 'inline-block'; // Or 'block', depending on your layout
                 // Ensure full content is hidden and preview is shown initially
                 fullContent.style.display = 'none';
                 preview.style.display = 'block';
                 showMoreLink.textContent = 'Show More'; // Reset text in case of caching issues
            } else {
                // Hide the link if content is short or doesn't need expanding
                showMoreLink.style.display = 'none';
                // Ensure full content is shown if there's no preview/link needed
                fullContent.style.display = 'block';
                preview.style.display = 'none'; // Hide preview if full content is shown by default
            }

            // --- Existing click event listener ---
            showMoreLink.addEventListener('click', function(event) {
                event.preventDefault(); // Prevent the default link behavior

                // Find the closest parent element with the class 'note-card'
                // This ensures we are working with the specific card that contains the clicked link
                const card = event.target.closest('.note-card'); 

                if (card) {
                    // Find the preview and full content elements *within this specific card*
                    const currentPreview = card.querySelector('.note-content-preview');
                    const currentFullContent = card.querySelector('.note-content-full');
                    const currentLink = card.querySelector('.show-more-link');
                    
                    if (currentPreview && currentFullContent && currentLink) {
                        // Toggle the display of the content sections
                        if (currentFullContent.style.display === 'none' || currentFullContent.style.display === '') {
                            currentPreview.style.display = 'none';
                            currentFullContent.style.display = 'block';
                            currentLink.textContent = 'Show Less'; // Change button text
                            card.classList.add('expanded'); // Optional: add a class for styling
                        } else {
                            currentFullContent.style.display = 'none';
                            currentPreview.style.display = 'block'; // Show preview again
                            currentLink.textContent = 'Show More'; // Change button text back
                            card.classList.remove('expanded'); // Optional: remove class
                        }
                    } else {
                         console.error('Could not find .note-content-preview or .note-content-full or .show-more-link within the card during click.');
                    }
                } else {
                    console.error("Could not find parent '.note-card' for the clicked link during click. Ensure your cards have this class or adjust the selector.");
                }
            });
        } else {
             console.error('Could not find preview, full content, or show more link for a note card.');
        }
    });
});