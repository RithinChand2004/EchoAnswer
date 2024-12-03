window.addEventListener('load', () => {
    setTimeout(() => {
      document.body.classList.add('loaded');
    }, 3000); // Adjust duration if needed
  });

  document.addEventListener('DOMContentLoaded', () => {
    // Initialize Bootstrap Popover
    const uploadButton = document.getElementById('uploadButton');
    new bootstrap.Popover(uploadButton, {
      trigger: 'click', // Popover appears on click
      placement: 'bottom', // Position the popover below the button
    });
  
    // Optional: Close the popover when clicking outside
    document.addEventListener('click', (event) => {
      if (!uploadButton.contains(event.target)) {
        bootstrap.Popover.getInstance(uploadButton)?.hide();
      }
    });
  });
  