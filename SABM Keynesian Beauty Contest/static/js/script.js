window.onload = function() {
    setTimeout(() => {
        let container = document.querySelector('.container');
        let letters = document.querySelectorAll('.initial .letter');
        let completes = document.querySelectorAll('.initial .complete');
        let whiteContainer = document.querySelector('.white-container');
        let startButton = document.querySelector('#start-button')

        // Dot fade out
        letters.forEach(letter => {
            let text = letter.textContent;
            letter.textContent = text.charAt(0);
        });

        // Show white container after letters and completes have moved
        // setTimeout(() => {
        //     whiteContainer.style.display = 'block';
        // }, 0);

        // Complete text fade in immediately
        completes.forEach(complete => {
            complete.style.opacity = '1';
            complete.style.transform = 'translateX(20px)';
            complete.style.lineHeight = '1.18';
        });

        // Move container slightly to the left
        container.style.transform = 'translateX(-150px)';

        // Change letters' color and background
        letters.forEach(letter => {
            letter.style.backgroundColor = 'white';
            letter.style.color = 'black';
            letter.style.fontWeight = '700';
            letter.style.transform = 'translateX(20px)'; // 只移动20px
            letter.style.lineHeight = '1.18';
        });

        setTimeout(() => {
            startButton.style.display = 'block';
        }, 0);

    }, 1200);

    document.getElementById('start-button').onclick = function() {
        window.location.href = '/main';
    };
};
