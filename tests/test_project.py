def test_about_route_returns_version(app_module):
    response = app_module.app.test_client().get("/")

    assert response.status_code == 200
    assert response.get_data(as_text=True) == "XemexPY: v0.0.1"


def test_price_route_fetches_price_and_posts_update(monkeypatch, app_module):
    requested_urls = []
    sent_messages = []

    class FakeResponse:
        def json(self):
            return {"BTC_XEM": {"last": "0.000123"}}

    def fake_get(url):
        requested_urls.append(url)
        return FakeResponse()

    monkeypatch.setattr(app_module.requests, "get", fake_get)
    monkeypatch.setattr(app_module, "WriteXem", sent_messages.append)

    response = app_module.app.test_client().get("/price")

    assert requested_urls == ["https://poloniex.com/public?command=returnTicker"]
    assert sent_messages == ["Latest price for BTC_XEM @ Poloniex : 0.000123"]
    assert response.get_data(as_text=True) == sent_messages[0]


def test_price_route_returns_empty_string_when_price_lookup_fails(monkeypatch, app_module):
    monkeypatch.setattr(app_module.requests, "get", lambda url: (_ for _ in ()).throw(RuntimeError("boom")))
    write_calls = []
    monkeypatch.setattr(app_module, "WriteXem", write_calls.append)

    response = app_module.app.test_client().get("/price")

    assert response.status_code == 200
    assert response.get_data(as_text=True) == ""
    assert write_calls == []


def test_writexem_ignores_empty_messages(app_module, fake_tweepy):
    app_module.WriteXem("")

    assert fake_tweepy.auth_instances == []
    assert fake_tweepy.api_instances == []


def test_writexem_posts_status_update(app_module, fake_tweepy):
    app_module.WriteXem("hello xem")

    assert len(fake_tweepy.auth_instances) == 1
    assert len(fake_tweepy.api_instances) == 1
    assert fake_tweepy.api_instances[0].auth is fake_tweepy.auth_instances[0]
    assert fake_tweepy.api_instances[0].updated_statuses == ["hello xem"]


def test_main_prints_expected_message(capsys, main_module):
    main_module.main()

    assert capsys.readouterr().out.strip() == "Hello from xemexpy!"


def test_clock_job_requests_price_endpoint(monkeypatch, clock_module):
    requested_urls = []
    monkeypatch.setattr(clock_module.requests, "get", requested_urls.append)

    clock_module.timed_job()

    assert requested_urls == ["https://xemexpy.herokuapp.com/price"]


def test_clock_job_swallows_request_errors(monkeypatch, clock_module):
    def boom(url):
        raise RuntimeError("boom")

    monkeypatch.setattr(clock_module.requests, "get", boom)

    clock_module.timed_job()