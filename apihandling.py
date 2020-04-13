from aiohttp import ClientSession
import asyncio


class managingAPI:
    def __init__(self):
        self._url_base = "https://pokeapi.co/api/v2/{0}/{1}"

    def url_creator(self, request):
        """
        for the search.
        """
        targetted_urls = []

        mode = request.mode.value

        for search in request.search_terms:

            targetted_urls.append(self._url_base.format(mode, search))

        return targetted_urls

    async def call_to_api(self, url, session: ClientSession):

        res = await session.request(method="GET", url=url)

        if res.status == 200:

            try:

                return await res.json()

            except ValueError as err:

                print(err)

        return None

    async def open_session(self, request_):

        all_tasks = []

        res = []

        statistic_result = []

        ab_results = []

        transport_results = []

        results_from_json = []

        async with ClientSession() as session:

            if len(request_.stat_urls) < 1:

                urls = self.url_creator(request_)

                for url in urls:
                    all_tasks.append(

                        asyncio.create_task(self.call_to_api(url, session)))

                results_from_json += await asyncio.gather(*all_tasks)

                results_from_json = [result for result in results_from_json if

                                     result is not {}]

            else:

                for poke_stats in request_.stat_urls:

                    for url in poke_stats:
                        all_tasks.append(asyncio.create_task(self.call_to_api(url,
                                                                              session)))

                    res += await asyncio.gather(*all_tasks)

                    statistic_result.append(res)

                    all_tasks = []

                    res = []

                results_from_json.append(statistic_result)

                for poke_stats in request_.ability_urls:

                    for url in poke_stats:
                        all_tasks.append(asyncio.create_task(self.call_to_api(url,
                                                                              session)))

                    res += await asyncio.gather(*all_tasks)

                    ab_results.append(res)

                    all_tasks = []

                    res = []
                results_from_json.append(ab_results)

                for poke_stats in request_.move_urls:

                    for url in poke_stats:
                        all_tasks.append(asyncio.create_task(self.call_to_api(url,
                                                                              session)))
                    res += await asyncio.gather(*all_tasks)

                    transport_results.append(res)

                    all_tasks = []

                    res = []

                results_from_json.append(transport_results)

            return results_from_json
