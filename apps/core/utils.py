import uuid6
import qrcode
import svgwrite


def get_square_size(matrix, start_row=0, start_col=0):
    size = 0
    n = len(matrix)

    # Count horizontally (row direction)
    while start_col + size < n and matrix[start_row][start_col + size]:
        size += 1

    # Verify vertically (column direction) to ensure it's actually a square
    for i in range(size):
        if not matrix[start_row + i][start_col]:
            return i  # stopped earlier

    return size


def generate_svg_qr(uuid, token, border=20, qr_code_radius=40) -> str:

    radius = 10

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=0,
    )

    qr.add_data(uuid)
    qr_matrix = qr.get_matrix()
    qr.make()
    img = qr.make_image(fill_color="black", back_color="white")

    img.save(open("qr_code.png", "wb"))
    qr_box_size = get_square_size(matrix=qr_matrix, start_col=0, start_row=0)

    height = len(qr_matrix) * 20 + (border * 2)
    width = len(qr_matrix) * 20 + (border * 2)

    dwg = svgwrite.Drawing("rounded_square.svg", size=(height, width))

    # x, y, width, height, rx (corner radius), ry (optional)
    dwg.add(
        dwg.rect(
            insert=(0, 0),
            size=(height, width),
            rx=qr_code_radius,
            ry=qr_code_radius,
            fill="#0B0A0C",
        )
    )

    total_qr_len = len(qr_matrix)

    start_pos = [border + radius, border + radius]

    for col_count, row in enumerate(qr_matrix):
        start_pos[0] = border + radius
        for row_count, cell in enumerate(row):
            if cell:
                if (
                    (row_count in range(qr_box_size, len(qr_matrix) - qr_box_size))
                    or (
                        row_count in range(0, qr_box_size)
                        and (
                            col_count
                            in range(qr_box_size, len(qr_matrix) - qr_box_size)
                        )
                    )
                    or row_count in range(len(qr_matrix) - qr_box_size, len(qr_matrix))
                    and (col_count in range(qr_box_size, len(qr_matrix)))
                ):
                    dwg.add(dwg.circle(center=start_pos, r=radius, fill="#B9C0CD"))

                if (
                    (row_count + 1 < qr_box_size and row_count > 0)
                    and (
                        (col_count + 1 < qr_box_size and col_count > 0)
                        or (
                            col_count > total_qr_len - qr_box_size
                            and col_count + 1 < total_qr_len
                        )
                    )
                ) or (
                    (
                        row_count > total_qr_len - qr_box_size
                        and row_count + 1 < total_qr_len
                    )
                    and (col_count + 1 < qr_box_size and col_count > 0)
                ):
                    dwg.add(dwg.circle(center=start_pos, r=radius, fill="#23C0DC"))

            start_pos[0] = (start_pos[0]) + (2 * radius)
        start_pos[1] = (start_pos[1]) + (2 * radius)

    dwg.add(
        dwg.rect(
            insert=(border + radius, border + radius),
            size=((qr_box_size - 1) * 20, (qr_box_size - 1) * 20),
            rx=qr_code_radius,
            ry=qr_code_radius,
            fill="none",
            stroke="#343B57",
            stroke_width=radius * 2,
        )
    )

    dwg.add(
        dwg.rect(
            insert=(width - qr_box_size * 20 - border + radius, border + radius),
            size=((qr_box_size - 1) * 20, (qr_box_size - 1) * 20),
            rx=qr_code_radius,
            ry=qr_code_radius,
            fill="none",
            stroke="#343B57",
            stroke_width=radius * 2,
        )
    )

    dwg.add(
        dwg.rect(
            insert=(border + radius, height - qr_box_size * 20 - border + radius),
            size=((qr_box_size - 1) * 20, (qr_box_size - 1) * 20),
            rx=qr_code_radius,
            ry=qr_code_radius,
            fill="none",
            stroke="#343B57",
            stroke_width=radius * 2,
        )
    )
    dwg.save()

    return dwg.tostring()
