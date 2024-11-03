// Set the event date and time (replace with your event details)
const eventDate = new Date('March 27, 2024 17:00:00 GMT+00:00').getTime();

// Update the countdown every second
const countdownInterval = setInterval(updateCountdown, 1000);

function updateCountdown() {
    const currentDate = new Date().getTime();
    const timeDifference = eventDate - currentDate;

    if (timeDifference <= 0) {
        // Event has already occurred, display a message
        clearInterval(countdownInterval);
        document.getElementById('countdown').innerHTML = 'Event is over! Checkout other upcoming event!';
    } else {
        const days = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
        const hours = Math.floor((timeDifference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((timeDifference % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((timeDifference % (1000 * 60)) / 1000);
        document.getElementById('countdown').innerHTML = `${days}d ${hours}h ${minutes}m ${seconds}s`;
    }
}