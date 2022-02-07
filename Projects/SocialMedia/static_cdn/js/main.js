// document.getElementById('sortBy').addEventListener('change',(e)=>{
//     e.target.closest('form').submit()
// })

// document.getElementById('sortDirection').addEventListener('change',(e)=>{
//     e.target.closest('form').submit()
// })

// document.getElementById('perPage').addEventListener('change',(e)=>{
//     e.target.closest('form').submit()
// })


document.querySelectorAll('.btn-order-by').forEach((el)=>{
    el.addEventListener('click',(e)=>{
        orderBy = e.currentTarget.dataset.order
        orderDir = e.currentTarget.dataset.direction
    
        document.querySelector('input#order_by').value = orderBy
        document.querySelector('input#order_dir').value = orderDir
    
        document.getElementById('filterForm').submit()
    })
})

document.querySelectorAll('button.btn-delete-animal').forEach((el)=>{
    el.addEventListener('click',(e)=>{
        id = e.currentTarget.dataset.id
        
        fetchData(`/animals/${id}/delete`,'POST')
            .then((data)=>{
              el.closest('tr').style.display='none'
                document.getElementById('responseMessages').innerHTML=` <div class="my-3 delete-success-alert alert alert-success alert-dismissible fade show" role="alert">
                    <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Success:"><use xlink:href="#check-circle-fill"/></svg>            
                    ${data.message}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                  </div>`
            })
            .catch(error => {
                document.getElementById('responseMessages').innerHTML=`<div class="my-3 delete-error-alert alert alert-danger alert-dismissible fade show" role="alert">
                    <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Danger:"><use xlink:href="#exclamation-triangle-fill"/></svg>
                    ${error.message}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                  </div>`
            });
    })
})




// Fetch all the forms we want to apply custom Bootstrap validation styles to
var forms = document.querySelectorAll('.needs-validation')

// Loop over them and prevent submission
Array.prototype.slice.call(forms)
  .forEach(function (form) {
    form.addEventListener('submit', function (event) {
      if (!form.checkValidity()) {
        event.preventDefault()
        event.stopPropagation()
      }

      form.classList.add('was-validated')
    }, false)
  })




async function fetchData(url = '', method='GET', data={}) {

    if (method==='POST'){
        const response = await fetch(url, {
            method: method,
            headers: {
              'Content-Type': 'application/json',
              "X-CSRFToken": csrftoken
            },
            credentials: "same-origin",
            body: JSON.stringify(data),
          });

        if(!response.ok) {
          
          return response.json().then(error => { 
            throw new Error(JSON.stringify(error)) 
          })
        }

        return response.json()

    }else{
        const response = await fetch(url, {
            method: method,
            headers: {
              'Content-Type': 'application/json',
              "X-CSRFToken": csrftoken
            },
            credentials: "same-origin",
          });

        if(!response.ok) {
          return response.json().then(error => { 
            throw new Error(JSON.stringify(error)) 
          })
        }

        return response.json()
    }

    
}
  

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');


