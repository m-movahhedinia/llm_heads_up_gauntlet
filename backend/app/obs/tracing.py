#!/usr/bin/env python3
"""Author: mansour

Description:

"""

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def setup_tracing(service_name: str = "wordgame-backend"):
    provider = TracerProvider(resource=Resource.create({"service.name": service_name}))
    processor = BatchSpanProcessor(OTLPSpanExporter())  # OTLP endpoint from env OTEL_EXPORTER_OTLP_ENDPOINT
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)


def instrument_lcel(chain, span_name: str):
    from langchain_core.runnables import RunnableLambda

    tracer = trace.get_tracer("lcel")

    def _invoke(input):
        with tracer.start_as_current_span(span_name) as span:
            span.set_attribute("input.type", type(input).__name__)
            span.set_attribute("input.size", len(str(input)))
            out = chain.invoke(input)
            span.set_attribute("output.type", type(out).__name__)
            span.set_attribute("output.size", len(str(getattr(out, "content", out))))
            return out

    return RunnableLambda(_invoke)
