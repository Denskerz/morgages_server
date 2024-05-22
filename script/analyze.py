import matplotlib.pyplot as plt


def analyzing(total: int, success: int, failed: int, df_success: int, df_failed: int, type_errors: list):
    main_labels = ['Success', 'Failed']

    print(f"")
    print(f"{success + failed} == {total}?")
    print(f"success = {success} \nfailed = {failed}\ndf_success = {df_success}\ndf_failed = {df_failed} \n\n"
          f"empty_dataframe_error = {type_errors[0]}\ncheck_type_error = {type_errors[1]}\nprocessing_error = {type_errors[2]}\n"
          f"read_excel_error = {type_errors[3]}\n"
          f"get_appendix_dataframe_error = {type_errors[4]}\n")

    sizes = [success, failed]
    explode = (0.1, 0)

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=main_labels, autopct='%1.1f%%', shadow=True, explode=explode,
           wedgeprops={'lw': 1, 'ls': '--', 'edgecolor': 'k'})
    ax.axis("equal")

    main_labels_ = ['deposit_success', 'deposit_failed']

    sizes_ = [df_success, df_failed]
    explode_ = (0.1, 0)

    fig, ax = plt.subplots()
    ax.pie(sizes_, labels=main_labels_, autopct='%1.1f%%', shadow=True, explode=explode_,
           wedgeprops={'lw': 1, 'ls': '--', 'edgecolor': 'k'})
    ax.axis("equal")

    main_labels1 = ['empty_dataframe_error', 'check_type_error', 'processing_error',
                    'read_excel_error', 'get_appendix_dataframe_error']


    sizes1 = type_errors
    explode1 = (0.1, 0, 0.05, 0.1, 0)

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes1, labels=main_labels1, autopct='%1.1f%%', shadow=True, explode=explode1,
            wedgeprops={'lw': 1, 'ls': '--', 'edgecolor': 'k'})
    ax1.axis("equal")

    plt.show()
