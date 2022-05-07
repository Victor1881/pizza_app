const updateDrink = document.getElementsByClassName('update-drink');

for(let i = 0; i < updateDrink.length; i++){
    updateDrink[i].addEventListener('click', function (){
        const dId = this.dataset.d;
        const action = this.dataset.action;
        console.log('dId:', dId, 'action:', action)
        console.log('USER:', user)
        if (user === 'AnonymousUser'){
            console.log('User is not authenticated')
        }else{
            updateOrder(dId, action)
        }
    })
}


function updateOrder(dId, action) {
    console.log('User is logged in, sending data..')

    const url = '/update_drink/'

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-type':'application/json',
            'Accept': 'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'dId': dId, 'action':action})
    })

    .then((response) =>{
            return response.json()
    })

        .then((drink) =>{
            console.log('drink:', drink)
            location.reload()
        })

}