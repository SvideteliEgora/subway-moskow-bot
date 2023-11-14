def json_converter(data: list) -> list[dict]:
    row_with_headers = data[0][:len(data[0]) - 2]
    rows_with_data = data[1:]
    deleted_value_indexes = []
    headers = ['id']
    for ind, header in enumerate(row_with_headers):
        if header:
            headers.append(header)
            continue
        deleted_value_indexes.append(ind)
    ID = 1
    res = []
    for row in rows_with_data:
        data_dict = {}
        i = 0
        for del_ind, item in enumerate(row[:len(row) - 2]):
            if i == 0:
                data_dict[headers[i]] = ID
            elif del_ind in deleted_value_indexes:
                continue
            else:
                data_dict[headers[i]] = item
            i += 1
        res.append(data_dict)
        ID += 1
    return res


def next_step(step=0) -> int:
    return step + 1



