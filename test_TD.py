from terminal_dashboard import TerminalDashboard, PrintBlock, assigning_attrib


if __name__ == "__main__":
    deb = TerminalDashboard()

    for i in range(10000000):
        all_blocks = []
        color = deb.NOMINAL

        # Block 1
        block = PrintBlock()
        block.title = "POSITION:"
        block.string_with_attrib = [
            ["---", color],
            [block.title, color],
            [f" Position    : {i}", color],
            [f" Orientation : {i}", color],
            [f" Velocity    : {i}", color],
        ]
        all_blocks.append(block)

        # Block 2
        flag = False
        block = PrintBlock()
        block.title = "SAFETY:"
        block.string_with_attrib = [
            ["---", color],
            [block.title, color],
            [f" Position : {i}", color],
            [f" Flag     : {flag}", assigning_attrib(flag)],
            [f" Velocity : {i}", color],
        ]
        all_blocks.append(block)

        # Block 3
        block = PrintBlock()
        block.title = "ANOTHER"
        block.string_with_attrib = [
            ["---", color],
            [block.title, color],
            [f" Position    : {i}", color],
            [f" Orientation : {i}", color],
            [f" Velocity    : {i}", color],
        ]
        all_blocks.append(block)

        # # Block 4
        # block = PrintBlock()
        # block.title = "YET ANOTHER"
        # block.string_with_attrib = [
        #     ["---", color],
        #     [block.title, color],
        #     [f" Position    : {i}", color],
        #     [f" Orientation : {i}", color],
        #     [f" Velocity    : {i}", color],
        # ]
        # all_blocks.append(block)

        # # Block 5
        # block = PrintBlock()
        # block.title = "FINAL"
        # block.string_with_attrib = [
        #     ["---", color],
        #     [block.title, color],
        #     [f" Position    : {i}", color],
        #     [f" Orientation : {i}", color],
        #     [f" Velocity    : {i}", color],
        # ]
        # all_blocks.append(block)

        # Printing
        deb.print_info(all_blocks, 1)

        deb.all_refresh()
        deb.all_erase()

        # Drawing bars
        bar = i / 100000
        bar2 = (i + 15) / 100000

        bar = 1 if bar > 1 else bar
        bar2 = 1 if bar2 > 1 else bar2

        deb.draw_bar(
            title="Actual Speed: ", value=bar, color=deb.BAR_YELLOW, attrib="normal"
        )

        deb.draw_bar(
            title="Gained Speed: ", value=bar2, color=deb.BAR_YELLOW, attrib="normal"
        )
        deb.draw_vertical_bar(
            title="vz ", value=bar, color=deb.BAR_WHITE, attrib="normal", start_row=50
        )

        deb.draw_vertical_bar(
            title="vy ", value=0.5, color=deb.BAR_YELLOW, attrib="normal", start_row=55
        )

        # deb.draw_vertical_bar(
        #     title="vx ", value=0.8, color=deb.BAR_WHITE, attrib="normal"
        # )

        # deb.all_refresh()
        # deb.all_erase()

    # deb.cleanup()
