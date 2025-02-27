const component = await electron.getAllWidgets()


let widgetList = component.widgets
for (const widget of widgetList) {
  widget.content = () => import(widget.relpath)
}


export const categorys = component.categorys
export const widgets = widgetList
export const number = component.number
