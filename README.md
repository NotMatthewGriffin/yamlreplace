# yamlreplace

This is small tool to replace values in a potentially nested yaml map.

It takes the input yaml from stdin or a file and then outputs it to stdout.

To use it either redirect or pipe in a yaml file like, and provide space separated replacement values:

```
./yamlreplace x.x:10 < test.yaml
cat test.yaml | ./yamlreplace x.x:10
```

If no input if redirected then `yamlreplace` will attempt to parse the first argument as a yaml file name.
This can be used like:

```
./yamlreplace test.yaml x.x:10
```
