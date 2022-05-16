def check_join_data(data):
    keys = ["roomname", "name", "location", "creator_options"]
    data_keys = data.keys()

    if not all(i in data_keys for i in keys):
        return False

    if not "currently_watching" in data["creator_options"]:
        return False

    return True


if __name__ == "__main__":
    print(
        check_join_data(
            {
                "roomname": "test",
                "name": "test",
                "location": "test",
                "creator_options": {"currently_watching": "Test"},
            }
        )
    )
    print(
        check_join_data(
            {
                "_roomname": "test",
                "name": "test",
                "location": "test",
                "creator_options": {"_currently_watching": "Test"},
            }
        )
    )
