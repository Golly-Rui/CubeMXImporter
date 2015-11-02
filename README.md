# CubeMXImporter
This tool can be used to import projects generated by STM32CubeMX tool inside an Eclipse project created with the GNU ARM Eclipse plugin. 

It can be easily used in this way:

1. Generate a new Eclipse project using the GNU ARM Eclipse plugin as described in [this blog post](http://www.carminenoviello.com/en/2015/06/04/stm32-applications-eclipse-gcc-stcube/) or in [this book](https://leanpub.com/mastering-stm32).
	1. Close the prject once generated
2. Create a new CubeMX project for your MCU or development board.
	2. Generate the C code from CubeMX project selecting SW4STM32 as Tool-chain.
3. Launch the CubeMXImporter tool with the following command:

```
$ python cubemximporter.py <path-to-eclipse-project> <path-to-cubemx-project>

```

4. Open again the Eclipse project and do a refresh of the source tree.

The whole procedure is better described [here]()

CubeMXImporter required `lxml`. You can install it using pip:

```
$ pip install lxml

```