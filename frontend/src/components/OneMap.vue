<template>
  <div>
    <canvas class="map-canvas" ref="canvas" />
  </div>
</template>

<script>
export default {
  name: "entry",
  data() {
    return {
      mapDimension: 512
    };
  },
  computed: {
    staticMapLink() {
      return `https://developers.onemap.sg/commonapi/staticmap/getStaticImage?layerchosen=default&lat=${this.location.lat}&lng=${this.location.long}&zoom=18&height=${this.mapDimension}&width=${this.mapDimension}`;
    }
  },
  props: {
    location: {
      type: Object,
      default: () => ({
        lat: 0,
        long: 0
      })
    }
  },
  methods: {
    loadImageOnCanvasCtx(img, ctx) {
      ctx.drawImage(img, 0, 0);
      ctx.arc(
        this.mapDimension / 2,
        this.mapDimension / 2,
        150,
        0,
        2 * Math.PI
      );
      ctx.strokeStyle = "rgba(44, 115, 201, 0.5)";
      ctx.lineWidth = 3;
      ctx.stroke();
      ctx.fillStyle = "rgba(179, 212, 252, 0.2)";
      ctx.fill();
    }
  },
  mounted() {
    const img = new Image();
    img.src = this.staticMapLink;
    this.$refs.canvas.height = this.mapDimension;
    this.$refs.canvas.width = this.mapDimension;
    const ctx = this.$refs.canvas.getContext("2d");
    img.onload = () => {
      this.loadImageOnCanvasCtx(img, ctx);
    };
  }
};
</script>
<style scoped>
.map-canvas {
  width: 100%;
}
</style>
