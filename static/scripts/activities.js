
$('.edit-button').click( (e) => {
    console.log('Edit button clicked!  ')
    const button = $(e.target)
    const garmin_id = button.attr('data-id')
    console.log(garmin_id)
})

$('.delete-button').click( (e) => {
    console.log('Delete button clicked!  ')
    const button = $(e.target)
    const garmin_id = button.attr('data-id')
    console.log(garmin_id)

    
})