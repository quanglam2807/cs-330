// Quang Lam

function printNumberContent(docParent, num, desc) {
    const card = document.createElement("div");
    card.className = "card";

    const body = document.createElement("div");
    body.className = "card-body";

    const h5 = document.createElement("h5");
    h5.className = "card-title";
    h5.innerText = num;

    const p = document.createElement("p");
    p.className = "card-text";
    p.innerText = desc;

    body.appendChild(h5);
    body.appendChild(p);

    card.appendChild(body);

    br = document.createElement("br");

    docParent.appendChild(card);
    docParent.appendChild(br);
}

async function getData(number) {
    return fetch("http://numbersapi.com/" + number)
        .then(response => response.text())
        .catch(error => console.log(error));
}

async function getInfo() {
    if (!document.querySelector("#number").value) return;

    const num = parseInt(document.querySelector("#number").value);

    const [n_minus_1, n, n_plus_1] = await Promise.all([
        getData(num - 1),
        getData(num),
        getData(num + 1)
    ]);

    const content = document.querySelector("#content");
    content.innerHTML = "";
    printNumberContent(content, num - 1, n_minus_1);
    printNumberContent(content, num, n);
    printNumberContent(content, num + 1, n_plus_1);
};

$(document).ready(function () {
    document.querySelector("#getInfo").addEventListener("click", getInfo);
});