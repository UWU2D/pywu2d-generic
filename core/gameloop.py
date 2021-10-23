from timeit import default_timer as timer
import time


def main_loop(service_factory, tick_rate):

    event_service = service_factory.event_service()
    render_service = service_factory.render_service()
    ui_service = service_factory.ui_service()
    input_service = service_factory.input_service()
    game_service = service_factory.game_service()

    input_service.initialize(event_service)
    render_service.initialize(game_service.resolution)
    ui_service.initialize(render_service, event_service)
    game_service.initialize(event_service, input_service,
                            render_service, ui_service)

    period = 1 / tick_rate

    exit = False

    def quit():
        nonlocal exit
        exit = True

    event_service.register_quit(quit)

    last_tick = timer()
    while not exit:
        start = timer()

        render_service.pre()
        ui_service.pre()

        event_service.maintain(timer() - last_tick)
        ui_service.maintain(timer() - last_tick)
        game_service.maintain(timer() - last_tick)

        ui_service.draw(render_service)
        render_service.render(game_service.sprites)

        ui_service.post()
        render_service.post()

        end = timer()

        to_sleep = period - (end - start)
        if to_sleep > 0:
            time.sleep(period - (end - start))

    ui_service.stop()
    render_service.stop()
    game_service.stop()
