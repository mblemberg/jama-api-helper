# Jama API for Python

## Dependencies

Only standard python 3 modules.

## Usage

Create a JamaInterface object by specifying the API endpoint URL for your specific cloud instance.

```python
jama = JamaInterface(
    endpoint_url='https://your_cloud_instance_here.jamacloud.com/rest/latest')
```

Authenticate using your client ID and client secret, which are generated within the Jama web application under user settings

```python
jama.authenticate(client_id=jama_client_id,
                    client_secret=jama_client_secret)
```

Retrieve an item from Jama by specifying the project ID and item ID

```python
item = jama.get_item(project_id=128, item_project_id='MY-REQ-101')
```

Print a string representation of the Jama item

```python
print(item)
```

Print all fields of the Jama item

```python
item.print_fields()
```
