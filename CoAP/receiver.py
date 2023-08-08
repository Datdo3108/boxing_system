import aiocoap
import asyncio

# Define a resource handler class that inherits from aiocoap.resource.Resource
class DataResource(aiocoap.resource.Resource):
    # Define an asynchronous method that handles POST requests
    async def render_post(self, request):
        # Get the request payload as a string
        data = request.payload.decode()

        # Print the data
        print(data)

        # Return an empty response with a success code
        return aiocoap.Message(code=aiocoap.CHANGED)

# Define an asynchronous function that creates and runs a CoAP server with the resource handler class
async def main():
    # Create a CoAP protocol object
    protocol = await aiocoap.Context.create_server_context()

    # Create a resource handler object with the name "data"
    resource = DataResource()

    # Add the resource handler object to the protocol object with the path "/data"
    protocol.add_resource(('data',), resource)

    # Wait indefinitely for incoming requests and handle them
    await asyncio.sleep_forever()

# Run the main function using the asyncio event loop
asyncio.run(main())
