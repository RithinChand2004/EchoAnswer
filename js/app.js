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
// Usage Statistics Chart
const ctx = document.getElementById('usageChart').getContext('2d');
const usageChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: ['2023-12-01', '2023-12-02', '2023-12-03', '2023-12-04'], // Dates for x-axis
    datasets: [{
      label: 'Chats per Day',
      data: [5, 8, 3, 10], // Number of chats for y-axis
      backgroundColor: 'rgba(102, 45, 140, 0.2)',
      borderColor: '#662D8C',
      borderWidth: 2,
      pointBackgroundColor: '#ED1E79',
      pointBorderColor: '#fff',
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: '#ED1E79',
      tension: 0.4, // Curve for the line
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: {
        display: true,
        position: 'top'
      }
    },
    scales: {
      x: {
        title: {
          display: true,
          text: 'Date'
        }
      },
      y: {
        title: {
          display: true,
          text: 'Number of Chats'
        },
        beginAtZero: true
      }
    }
  }
});  