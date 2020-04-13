import AllRequests as req

import asyncio


class pokemondex:
    """
    main driver class .
    """

    def __init__(self):
        """
        Init for this class
        """
        extension_file = req.ExtensionHandler()

        http_handle = req.HttpHandler()

        handle_subquery = req.SubqueryHandler()

        http_handle_sub = req.HttpHandler()

        handle_json_sub = req.JsonQueryHandler()

        config_file = req.ExtensionHandler()

        config_http = req.HttpHandler()

        config_json = req.JsonHandler()

        config_print = req.OutcomeHandler()

        self._expand_start_handler = extension_file

        extension_file.next_handler = http_handle

        http_handle.next_handler = handle_subquery

        handle_subquery.next_handler = http_handle_sub

        http_handle_sub.next_handler = handle_json_sub

        self._concise_start_handler = config_file

        config_file.next_handler = config_http

        config_http.next_handler = config_json

        config_json.next_handler = config_print

    async def exec_req(self, request: req.Req) -> None:
        """
        handles request through a chain of handlers
        """
        if request.is_expanded:

            return await self._expand_start_handler.handle_request(request)
        else:
            return await self._concise_start_handler.handle_request(request)


def main():
    somereq = req.ReqHandle.set_the_cli_req()

    runner = pokemondex()
    try:

        asyncio.run(runner.exec_req(somereq))

    except Exception as err:

        print(err)


if __name__ == "__main__":

    main()
