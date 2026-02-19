from bank_ui.display import Display

cols = {"id": 1, "bank_id":2, "owner":3, "balance":2, "acc_id":5}
cols2 = [{"id": 1, "bank_id":2, "owner":3, "balance":2, "acc_id":5},
         {"id": 1, "bank_id":2, "owner":3, "balance":2, "acc_id":5}]

display = Display()
display.display_content(cols)
