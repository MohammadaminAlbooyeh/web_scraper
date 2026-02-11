document.getElementById('start-scraping').addEventListener('click', async () => {
    const response = await fetch('http://127.0.0.1:8000/start-scraping', {
        method: 'POST'
    });
    const result = await response.json();
    alert(result.message);
});

async function fetchData() {
    const response = await fetch('http://127.0.0.1:8000/data');
    const data = await response.json();

    const dataList = document.getElementById('data-list');
    dataList.innerHTML = '';

    data.data.forEach(item => {
        const li = document.createElement('li');
        li.textContent = JSON.stringify(item);
        dataList.appendChild(li);
    });
}

// Fetch data on page load
fetchData();

document.getElementById('scraping-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const urlInput = document.getElementById('url-input').value;

    const response = await fetch('http://127.0.0.1:8000/start-scraping', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: urlInput }),
    });

    const result = await response.json();
    alert(result.message);
});