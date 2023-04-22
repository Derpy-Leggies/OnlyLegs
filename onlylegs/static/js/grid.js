function makeGrid() {
    // Get the container and images
    const container = document.querySelector('.gallery-grid');
    const images = document.querySelectorAll('.gallery-item');

    // Set the gap between images
    const gap = 0.6 * 16;
    const maxWidth = container.clientWidth - gap;
    const maxHeight = 13 * 16;

    // Calculate the width and height of each image
    let calculated = {};
    for (let i = 0; i < images.length; i++) {
        const image = images[i].querySelector('img');
        const width = image.naturalWidth;
        const height = image.naturalHeight;

        let ratio = width / height;
        const newWidth = maxHeight * ratio;

        if (newWidth > maxWidth) {
            newWidth = maxWidth / 3 - gap; // 3 images per row max
            ratio = newWidth / height;
        }

        calculated[i] = {"width": newWidth,
                         "height": maxHeight,
                         "ratio": ratio};
    }

    // Next images position
    let nextTop = gap;
    let nextLeft = gap;

    for (let i = 0; i < images.length; i++) {
        let currentRow = [];
        let currectLength = 0;

        // While the row is not full add images to it
        while (currectLength < maxWidth) {
            currentRow.push(i);
            currectLength += calculated[i]["width"];
            i++;
        }
        // currentRow.push(i);
        // currectLength += calculated[i]["width"];

        // Go back one image as it can't be added to the row
        i--;

        // Calculate the amount of space required to fill the row
        const currentRowDiff = (currectLength - maxWidth);

        // Cycle through the images in the row and adjust their width and left position
        for (let j = 0; j < currentRow.length; j++) {
            const image = images[currentRow[j]];
            const data = calculated[currentRow[j]];
            // Shrink compared to the % of the row it takes up
            const shrink = currentRowDiff * (data["width"] / currectLength);

            image.style.width = data["width"] - shrink - gap + 'px';
            image.style.height = data["height"] + 'px';
            image.style.left = nextLeft + 'px';
            image.style.top = nextTop + 'px';

            nextLeft += data["width"] - shrink;
        }

        // Reset for the next row
        nextTop += maxHeight + gap;
        nextLeft = gap;
    }
}