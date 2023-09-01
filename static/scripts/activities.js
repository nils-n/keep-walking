
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
    // console.log(.attr('data-id'))
    // const garmin_data_id = $(this).siblings('.garmin-id')
    // const garmin_data_id_for_delete = garmin_data_id[0]
    // console.log(garmin_data_id)
    // console.log(garmin_data_id_for_delete)

})