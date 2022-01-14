const close_btn = document.querySelector('#CloseModal');
const close_btn2 = document.querySelector('#CloseModal2');
const tabelOutput = document.querySelector('.table-output');
const appTable = document.querySelector('.app-table');
const PaginationContainer = document.querySelector('.pagination-container');
const tbody = document.querySelector(".tableBody")
const noresult = document.querySelector(".no-result")
tabelOutput.style.display = "none";
var id;
function openModal(val) {
    document.querySelector(".modal").classList.add("show");
    document.querySelector(".modal").style.display = "block";
    id = val;
}
function close() {
    document.querySelector(".modal").classList.remove("show");
    document.querySelector(".modal").style.display = "";
}
function changeHref(aElem) {
    close();
    aElem.href = `expense-delete/${id}`;

}
close_btn.addEventListener("click", close);
close_btn2.addEventListener("click", close);

function MouseMove(id) {
    onmove = document.getElementById(id)
    onmove.classList.add("active");
}
function MouseLeave(id) {
    onmove = document.getElementById(id)
    onmove.classList.remove("active");
}

const Search = document.querySelector("#SearchField")

Search.addEventListener("keyup", (e) => {
    const searchval = e.target.value
    if (searchval.trim().length > 0) {
        PaginationContainer.style.display = "none";
        fetch("/search-expense", {
            body: JSON.stringify({ searchText: searchval }),
            method: "POST",
        })
            .then((res) => res.json())
            .then((data) => {
                tbody.innerHTML = "";
                console.log(data)
                appTable.style.display = "none";
                tabelOutput.style.display = "block";
                console.log(data.length)
                if (data.length === 0) {
                    noresult.innerHTML = "No mathing results";
                    tabelOutput.style.display = "none";
                }
                else {
                    tabelOutput.style.display = "block";
                    noresult.innerHTML = "";
                    data.forEach(element => {
                        tbody.innerHTML += `
                        <tr>
                <td>${element.amount}</td>
                <td>${element.category}</td>
                <td>${element.description}</td>
                <td>${element.date}</td>
                <td><a href="{% url 'expense_edit' exp.id %}" class="btn btn-outline-success btn-sm"><i
                  class="fad fa-edit"></i></a> <button type="button" onclick="openModal({{exp.id}});"
                class="btn btn-outline-danger btn-sm" id="modal_btn" data-toggle="modal"
                data-target="#exampleModalCenter">
                <i class="fal fa-trash-alt"></i>
              </button></td>
                </tr>
                        `
                        console.log(element.id);
                    });
                }
            });
    }
    else {
        tabelOutput.style.display = "none";
        appTable.style.display = "block";
        PaginationContainer.style.display = "block";
    }
})