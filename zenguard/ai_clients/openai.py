import httpx
from typing import Dict, Iterable, List, Literal, Union, override, Optional
from openai import NOT_GIVEN, NotGiven, OpenAI
from openai.resources.chat import Chat
from openai.resources.chat.completions import Completions
from openai._types import Body, Query, Headers
from openai.types.chat import completion_create_params, ChatCompletionToolParam, ChatCompletionToolChoiceOptionParam, ChatCompletionMessageParam
from openai._compat import cached_property


class CompletionsWithZenguard(Completions):
    def __init__(self, client: OpenAI, zenguard) -> None:
        self._zenguard = zenguard
        super().__init__(client)
    
    @override
    def create(
        self,
        *,
        detectors: list,
        messages: Iterable[ChatCompletionMessageParam],
        model: Union[
            str,
            Literal[
                "gpt-4-0125-preview",
                "gpt-4-turbo-preview",
                "gpt-4-1106-preview",
                "gpt-4-vision-preview",
                "gpt-4",
                "gpt-4-0314",
                "gpt-4-0613",
                "gpt-4-32k",
                "gpt-4-32k-0314",
                "gpt-4-32k-0613",
                "gpt-3.5-turbo",
                "gpt-3.5-turbo-16k",
                "gpt-3.5-turbo-0301",
                "gpt-3.5-turbo-0613",
                "gpt-3.5-turbo-1106",
                "gpt-3.5-turbo-0125",
                "gpt-3.5-turbo-16k-0613",
            ],
        ],
        frequency_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        function_call: completion_create_params.FunctionCall | NotGiven = NOT_GIVEN,
        functions: Iterable[completion_create_params.Function] | NotGiven = NOT_GIVEN,
        logit_bias: Optional[Dict[str, int]] | NotGiven = NOT_GIVEN,
        logprobs: Optional[bool] | NotGiven = NOT_GIVEN,
        max_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        n: Optional[int] | NotGiven = NOT_GIVEN,
        presence_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        response_format: completion_create_params.ResponseFormat | NotGiven = NOT_GIVEN,
        seed: Optional[int] | NotGiven = NOT_GIVEN,
        stop: Union[Optional[str], List[str]] | NotGiven = NOT_GIVEN,
        stream: Optional[Literal[False]] | NotGiven = NOT_GIVEN,
        temperature: Optional[float] | NotGiven = NOT_GIVEN,
        tool_choice: ChatCompletionToolChoiceOptionParam | NotGiven = NOT_GIVEN,
        tools: Iterable[ChatCompletionToolParam] | NotGiven = NOT_GIVEN,
        top_logprobs: Optional[int] | NotGiven = NOT_GIVEN,
        top_p: Optional[float] | NotGiven = NOT_GIVEN,
        user: str | NotGiven = NOT_GIVEN,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ):
        detect_response = None
        for message in messages:
            if message["role"] == "user" and message["content"] != "":
                detect_response = self._zenguard.detect(detectors=detectors, prompt=message["content"])
                if "error" in detect_response:
                    return detect_response
                if detect_response["is_detected"] is True:
                    if (
                        ("block" in detect_response and len(detect_response["block"]) > 0) or
                        ("score" in detect_response and detect_response["score"] == 1.0)
                    ):
                        return detect_response
        return super().create(
            messages=messages,
            model=model,
            frequency_penalty=frequency_penalty,
            function_call=function_call,
            functions=functions,
            logit_bias=logit_bias,
            logprobs=logprobs,
            max_tokens=max_tokens,
            n=n,
            presence_penalty=presence_penalty,
            response_format=response_format,
            seed=seed,
            stop=stop,
            stream=stream,
            temperature=temperature,
            tool_choice=tool_choice,
            tools=tools,
            top_logprobs=top_logprobs,
            top_p=top_p,
            user=user,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )

class ChatWithZenguard(Chat):
    def __init__(self, client: OpenAI, zenguard) -> None:
        self._zenguard = zenguard
        super().__init__(client)

    @cached_property
    def completions(self) -> CompletionsWithZenguard:
        return CompletionsWithZenguard(self._client, self._zenguard)
    

    